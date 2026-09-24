import json
import logging
from datetime import datetime
from openai import OpenAI
from django.conf import settings
from .models import Project, Task, ChatMessage

logger = logging.getLogger(__name__)

MODEL_NAME = getattr(settings, 'GEMINI_MODEL', 'gemini-3.6-flash')

FALLBACK_MODELS = [
    MODEL_NAME,
    'gemini-3.6-flash',
    'gemini-3.5-flash',
    'gemini-flash-latest',
    'gemini-3.1-flash-lite',
]

def _get_client():
    api_key = (
        getattr(settings, 'GEMINI_API_KEY', '') or
        getattr(settings, 'OPENAI_API_KEY', '') or
        os.getenv('GEMINI_API_KEY', '') or
        os.getenv('OPENAI_API_KEY', '')
    )
    if not api_key:
        raise ValueError(
            "Missing credentials! Please add the GEMINI_API_KEY environment variable in your Render Dashboard (under Environment Variables) or in your local .env file."
        )
    return OpenAI(
        api_key=api_key,
        base_url=getattr(settings, 'GEMINI_BASE_URL', 'https://generativelanguage.googleapis.com/v1beta/openai/'),
    )

def _call_gemini(messages_payload, tools=None):
    client = _get_client()
    seen = set()
    models_to_try = [m for m in FALLBACK_MODELS if not (m in seen or seen.add(m))]
    last_err = None
    for model in models_to_try:
        try:
            kwargs = {
                "model": model,
                "messages": messages_payload,
            }
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"
            return client.chat.completions.create(**kwargs)
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "resource_exhausted" in err_str or "quota" in err_str or "rate limit" in err_str:
                logger.warning(f"Model {model} hit rate limit/quota. Falling back to next model...")
                last_err = e
                continue
            raise e
    if last_err:
        raise last_err

# ==========================================
# Helpers for Flexible Entity Resolution
# ==========================================

def _find_project(user, project_id=None, project_title=None):
    if project_id:
        try:
            p = Project.objects.filter(id=int(project_id), user=user).first()
            if p:
                return p
        except (ValueError, TypeError):
            pass
    if project_title:
        query = str(project_title).strip()
        p = Project.objects.filter(user=user, title__iexact=query).first()
        if p:
            return p
        p = Project.objects.filter(user=user, title__icontains=query).first()
        if p:
            return p
    # Default fallback if user has exactly one project
    user_projects = Project.objects.filter(user=user)
    if user_projects.count() == 1:
        return user_projects.first()
    return None

def _find_task(user, task_identifier, project=None):
    if not task_identifier:
        return None
    # Check if identifier is numeric ID
    if isinstance(task_identifier, int) or (isinstance(task_identifier, str) and task_identifier.strip().isdigit()):
        try:
            tid = int(str(task_identifier).strip())
            qs = Task.objects.filter(id=tid, project__user=user)
            if project:
                qs = qs.filter(project=project)
            t = qs.first()
            if t:
                return t
        except (ValueError, TypeError):
            pass

    qs = Task.objects.filter(project__user=user)
    if project:
        qs = qs.filter(project=project)
    
    query = str(task_identifier).strip()
    t = qs.filter(title__iexact=query).first()
    if t:
        return t
    t = qs.filter(title__icontains=query).first()
    return t

# ==========================================
# Secure Tool Executions (Tenant Scoped)
# ==========================================

def list_projects(user, **kwargs):
    projects = Project.objects.filter(user=user).prefetch_related('tasks')
    data = []
    for p in projects:
        data.append({
            "id": p.id,
            "title": p.title,
            "status": p.status,
            "completion_percentage": p.completion_percentage,
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "is_completed": t.is_completed,
                    "priority": t.priority,
                    "assigned_to": t.assigned_to,
                    "due_date": str(t.due_date) if t.due_date else None
                } for t in p.tasks.all()
            ]
        })
    return json.dumps({"projects": data, "total_projects": len(data)})

def create_project(user, title, description="", **kwargs):
    title = str(title).strip()
    if not title:
        return json.dumps({"error": "Project title cannot be empty."})
    project = Project.objects.create(user=user, title=title, description=description or "")
    return json.dumps({"success": True, "project_id": project.id, "title": project.title})

def delete_project(user, project_id=None, title=None, **kwargs):
    project = _find_project(user, project_id=project_id, project_title=title)
    if not project:
        return json.dumps({"error": f"Project not found (searched for id={project_id}, title='{title}')."})
    project_title = project.title
    project.delete()
    return json.dumps({"success": True, "deleted_project": project_title})

def create_task(user, title, project_title=None, project_id=None, priority="MEDIUM", due_date=None, description="", assigned_to="", **kwargs):
    title = str(title).strip()
    if not title:
        return json.dumps({"error": "Task title cannot be empty."})

    project = _find_project(user, project_id=project_id, project_title=project_title)
    if not project:
        project = Project.objects.filter(user=user).first()
        if not project:
            project = Project.objects.create(user=user, title="General Tasks", description="Default project created automatically.")

    p_val = priority.upper() if priority and priority.upper() in Task.Priority.values else Task.Priority.MEDIUM
    task = Task.objects.create(
        project=project,
        title=title,
        description=description or "",
        due_date=due_date if due_date else None,
        priority=p_val,
        assigned_to=str(assigned_to).strip() if assigned_to else ""
    )
    return json.dumps({
        "success": True,
        "task_id": task.id,
        "title": task.title,
        "project": project.title,
        "priority": task.priority,
        "assigned_to": task.assigned_to
    })

def assign_task(user, task_identifier, project_identifier=None, assigned_to=None, **kwargs):
    task = _find_task(user, task_identifier)
    if not task:
        return json.dumps({"error": f"Task '{task_identifier}' not found."})

    changes = []
    if project_identifier:
        target_project = _find_project(user, project_title=project_identifier, project_id=project_identifier if str(project_identifier).isdigit() else None)
        if target_project:
            task.project = target_project
            changes.append(f"assigned to project '{target_project.title}'")
        else:
            return json.dumps({"error": f"Target project '{project_identifier}' not found."})

    if assigned_to is not None:
        task.assigned_to = str(assigned_to).strip()
        changes.append(f"assigned to @{task.assigned_to}" if task.assigned_to else "unassigned")

    task.save()
    return json.dumps({
        "success": True,
        "task_id": task.id,
        "title": task.title,
        "project": task.project.title,
        "assigned_to": task.assigned_to,
        "message": ", ".join(changes) if changes else "No changes made."
    })

def update_task_status(user, task_identifier, is_completed, **kwargs):
    task = _find_task(user, task_identifier)
    if not task:
        return json.dumps({"error": f"Task '{task_identifier}' not found."})
    task.is_completed = bool(is_completed)
    task.save()
    return json.dumps({"success": True, "task_id": task.id, "title": task.title, "is_completed": task.is_completed})

def delete_task(user, task_identifier, **kwargs):
    task = _find_task(user, task_identifier)
    if not task:
        return json.dumps({"error": f"Task '{task_identifier}' not found."})
    task_title = task.title
    task.delete()
    return json.dumps({"success": True, "deleted_task": task_title})

def delete_project_or_task(user, entity_type, entity_id=None, title=None, **kwargs):
    if entity_type.lower() == "project":
        return delete_project(user, project_id=entity_id, title=title)
    elif entity_type.lower() == "task":
        identifier = entity_id if entity_id is not None else title
        return delete_task(user, task_identifier=identifier)
    return json.dumps({"error": f"Invalid entity_type: {entity_type}"})

AVAILABLE_TOOLS = {
    "list_projects": list_projects,
    "create_project": create_project,
    "delete_project": delete_project,
    "create_task": create_task,
    "assign_task": assign_task,
    "update_task_status": update_task_status,
    "delete_task": delete_task,
    "delete_project_or_task": delete_project_or_task,
}

# ==========================================
# Tool Schemas for Model Integration
# ==========================================

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_projects",
            "description": "Retrieve all projects along with tasks, statuses, priorities, assignees, and progress percentages.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_project",
            "description": "Create a new project container for tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title or name of the project."},
                    "description": {"type": "string", "description": "Optional project description or goals."}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_project",
            "description": "Delete an existing project and all its associated tasks by title or ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Name/title of the project to delete."},
                    "project_id": {"type": "integer", "description": "Numeric database ID of the project to delete (optional if title is provided)."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new task under a project.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the task."},
                    "project_title": {"type": "string", "description": "Name/title of the project to add the task to (optional)."},
                    "project_id": {"type": "integer", "description": "Database ID of the project (optional if project_title is provided)."},
                    "priority": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"], "description": "Task priority level."},
                    "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format (optional)."},
                    "assigned_to": {"type": "string", "description": "Person or team member to assign the task to (optional)."},
                    "description": {"type": "string", "description": "Optional task details or acceptance criteria."}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "assign_task",
            "description": "Assign or move a task to a project, or assign it to a team member / person.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_identifier": {"type": "string", "description": "Title or numeric ID of the task to assign."},
                    "project_identifier": {"type": "string", "description": "Project title or ID to move the task into (optional)."},
                    "assigned_to": {"type": "string", "description": "Name or username of the person to assign the task to (optional)."}
                },
                "required": ["task_identifier"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task_status",
            "description": "Mark a task complete or incomplete by its title or ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_identifier": {"type": "string", "description": "Title or ID of the task."},
                    "is_completed": {"type": "boolean", "description": "True to mark done/completed, False to mark pending."}
                },
                "required": ["task_identifier", "is_completed"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task by its title or ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_identifier": {"type": "string", "description": "Title or ID of the task to delete."}
                },
                "required": ["task_identifier"]
            }
        }
    }
]

# ==========================================
# Agent Core Loop
# ==========================================

def run_agent_turn(user, user_prompt: str) -> tuple[str, bool]:
    """
    Executes a multi-turn tool call resolution loop.
    Returns: (final_assistant_message, did_mutate_state)
    """
    # 1. Save user prompt
    ChatMessage.objects.create(user=user, role=ChatMessage.Role.USER, content=user_prompt)

    # 2. Rebuild clean conversational history (only text turns from past messages)
    past_messages = (
        ChatMessage.objects.filter(user=user, role__in=[ChatMessage.Role.USER, ChatMessage.Role.ASSISTANT])
        .exclude(content='')
        .order_by('-created_at')[:8]
    )

    messages_payload = [
        {
            "role": "system",
            "content": (
                f"You are an intelligent, friendly, and proactive AI Project Management Chatbot Assistant. "
                f"Today's date is {datetime.now().strftime('%Y-%m-%d')}.\n\n"
                "Capabilities:\n"
                "- You converse naturally with the user, answer questions, provide productivity advice, and help organize work.\n"
                "- You have full control over the user's projects and tasks using the provided tools.\n"
                "- When the user asks to add, create, delete, list, or assign projects or tasks, ALWAYS call the corresponding tools.\n"
                "- You can identify projects and tasks by name/title or by numeric ID.\n"
                "- Format your answers with clean Markdown (bold text, bullet points, numbered lists) so they look great.\n"
                "- After executing tools, summarize clearly what was done."
            )
        }
    ]

    for m in reversed(list(past_messages)):
        messages_payload.append({
            "role": m.role,
            "content": m.content
        })

    did_mutate = False
    max_turns = 5
    try:
        for _ in range(max_turns):
            response = _call_gemini(messages_payload, tools=TOOL_SCHEMAS)
            response_msg = response.choices[0].message

            if not response_msg.tool_calls:
                final_reply = response_msg.content or "Completed."
                ChatMessage.objects.create(user=user, role=ChatMessage.Role.ASSISTANT, content=final_reply)
                return final_reply, did_mutate

            # Directly append response_msg object to preserve Google thought signatures
            messages_payload.append(response_msg)

            for tool_call in response_msg.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments or "{}")

                if fn_name in ["create_project", "delete_project", "create_task", "assign_task", "update_task_status", "delete_task", "delete_project_or_task"]:
                    did_mutate = True

                fn_impl = AVAILABLE_TOOLS.get(fn_name)
                if fn_impl:
                    try:
                        tool_result = fn_impl(user=user, **fn_args)
                    except Exception as tool_err:
                        logger.error(f"Error executing tool {fn_name}: {tool_err}")
                        tool_result = json.dumps({"error": str(tool_err)})
                else:
                    tool_result = json.dumps({"error": f"Unknown tool: {fn_name}"})

                messages_payload.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": fn_name,
                    "content": tool_result
                })

        return "Operation completed.", did_mutate

    except Exception as e:
        logger.error(f"Error in run_agent_turn: {e}", exc_info=True)
        error_reply = f"Sorry, I encountered an issue while processing your request: {str(e)}"
        ChatMessage.objects.create(user=user, role=ChatMessage.Role.ASSISTANT, content=error_reply)
        return error_reply, did_mutate