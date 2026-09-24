from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .models import Project, Task, ChatMessage
from .ai_agent import run_agent_turn

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def dashboard(request):
    projects = Project.objects.filter(user=request.user).prefetch_related('tasks')
    high_priority_tasks = Task.objects.filter(
        project__user=request.user, priority=Task.Priority.HIGH, is_completed=False
    )[:6]
    chat_history = ChatMessage.objects.filter(user=request.user).exclude(role='tool').order_by('created_at')[:20]

    return render(request, "dashboard.html", {
        "projects": projects,
        "high_priority_tasks": high_priority_tasks,
        "chat_history": chat_history
    })

@login_required
def project_board_partial(request):
    projects = Project.objects.filter(user=request.user).prefetch_related('tasks')
    return render(request, "partials/project_board.html", {"projects": projects})

@login_required
def urgent_tasks_partial(request):
    high_priority_tasks = Task.objects.filter(
        project__user=request.user, priority=Task.Priority.HIGH, is_completed=False
    )[:6]
    return render(request, "partials/urgent_tasks.html", {"high_priority_tasks": high_priority_tasks})

@login_required
@require_POST
def create_task(request):
    project_id = request.POST.get("project_id")
    title = request.POST.get("title", "").strip()
    priority = request.POST.get("priority", Task.Priority.MEDIUM)
    due_date = request.POST.get("due_date", "").strip() or None
    description = request.POST.get("description", "").strip()

    if not title or not project_id:
        return HttpResponse("Title and Project are required.", status=400)

    project = get_object_or_404(Project, id=project_id, user=request.user)

    if priority not in Task.Priority.values:
        priority = Task.Priority.MEDIUM

    Task.objects.create(
        project=project,
        title=title,
        description=description,
        priority=priority,
        due_date=due_date
    )

    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'projectStateChanged'
    return response

@login_required
@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__user=request.user)
    task.delete()
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'projectStateChanged'
    return response

@login_required
@require_POST
def create_project(request):
    title = request.POST.get("title", "").strip()
    description = request.POST.get("description", "").strip()
    if not title:
        return HttpResponse("Title is required.", status=400)
    Project.objects.create(user=request.user, title=title, description=description)
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'projectStateChanged'
    return response

@login_required
@require_POST
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    response = render(request, "partials/task_item.html", {"task": task})
    response['HX-Trigger'] = 'projectStateChanged'
    return response

@login_required
@require_POST
def send_chat(request):
    prompt = request.POST.get("message", "").strip()
    if not prompt:
        return HttpResponse(status=400)

    assistant_reply, did_mutate = run_agent_turn(request.user, prompt)
    
    response = render(request, "partials/chat_message_turn.html", {
        "user_message": prompt,
        "assistant_message": assistant_reply
    })
    
    if did_mutate:
        response['HX-Trigger'] = 'projectStateChanged'
    
    return response

@login_required
@require_POST
def clear_chat(request):
    ChatMessage.objects.filter(user=request.user).delete()
    return render(request, "partials/chat_stream.html", {"chat_history": []})

