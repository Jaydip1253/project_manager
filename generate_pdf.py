import os
import subprocess
from pathlib import Path

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AgentPM - Complete Project & AI Architecture Documentation</title>
  <style>
    @page {
      size: A4;
      margin: 16mm 14mm;
      @bottom-right {
        content: counter(page);
      }
    }
    
    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #1e293b;
      background-color: #ffffff;
      line-height: 1.55;
      font-size: 11pt;
      margin: 0;
      padding: 0;
    }

    /* Cover / Header */
    .doc-header {
      background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #0369a1 100%);
      color: #ffffff;
      padding: 32px 28px;
      border-radius: 12px;
      margin-bottom: 28px;
    }

    .doc-badge {
      display: inline-block;
      background: rgba(56, 189, 248, 0.2);
      border: 1px solid rgba(56, 189, 248, 0.4);
      color: #38bdf8;
      font-size: 8.5pt;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 4px 10px;
      border-radius: 9999px;
      margin-bottom: 12px;
    }

    .doc-title {
      font-size: 24pt;
      font-weight: 800;
      line-height: 1.2;
      margin: 0 0 10px 0;
      letter-spacing: -0.02em;
    }

    .doc-subtitle {
      font-size: 11.5pt;
      color: #94a3b8;
      margin: 0 0 18px 0;
      line-height: 1.4;
    }

    .doc-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      font-size: 8.5pt;
      color: #cbd5e1;
      border-top: 1px solid rgba(255, 255, 255, 0.15);
      padding-top: 14px;
    }

    .doc-meta-item strong {
      color: #38bdf8;
    }

    /* Headings */
    h1 {
      font-size: 16pt;
      font-weight: 800;
      color: #0f172a;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 6px;
      margin-top: 26px;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    h2 {
      font-size: 13pt;
      font-weight: 700;
      color: #1e293b;
      margin-top: 18px;
      margin-bottom: 8px;
    }

    h3 {
      font-size: 11pt;
      font-weight: 700;
      color: #334155;
      margin-top: 14px;
      margin-bottom: 6px;
    }

    p {
      margin: 0 0 10px 0;
      color: #334155;
    }

    /* Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0;
      font-size: 9.5pt;
      page-break-inside: avoid;
    }

    th {
      background-color: #0f172a;
      color: #f8fafc;
      font-weight: 700;
      text-align: left;
      padding: 8px 10px;
      border: 1px solid #0f172a;
    }

    td {
      padding: 7px 10px;
      border: 1px solid #cbd5e1;
      vertical-align: top;
    }

    tr:nth-child(even) td {
      background-color: #f8fafc;
    }

    /* Code & Blocks */
    code {
      font-family: "Cascadia Code", Consolas, "Courier New", monospace;
      font-size: 8.5pt;
      background-color: #f1f5f9;
      color: #0369a1;
      padding: 1.5px 4.5px;
      border-radius: 4px;
      border: 1px solid #e2e8f0;
    }

    pre {
      background-color: #0f172a;
      color: #e2e8f0;
      font-family: "Cascadia Code", Consolas, "Courier New", monospace;
      font-size: 8pt;
      line-height: 1.45;
      padding: 12px 14px;
      border-radius: 8px;
      overflow-x: auto;
      margin: 12px 0;
      page-break-inside: avoid;
      border: 1px solid #1e293b;
    }

    pre code {
      background: none;
      color: inherit;
      padding: 0;
      border: none;
      font-size: inherit;
    }

    /* Callout Boxes */
    .callout {
      border-radius: 8px;
      padding: 12px 14px;
      margin: 12px 0;
      font-size: 9.5pt;
      page-break-inside: avoid;
    }

    .callout-info {
      background-color: #f0f9ff;
      border-left: 4px solid #0284c7;
      color: #0369a1;
    }

    .callout-success {
      background-color: #f0fdf4;
      border-left: 4px solid #16a34a;
      color: #15803d;
    }

    .callout-warning {
      background-color: #fffbeb;
      border-left: 4px solid #d97706;
      color: #b45309;
    }

    .callout strong {
      display: block;
      margin-bottom: 4px;
      font-size: 10pt;
    }

    /* Architecture Flow Box */
    .flow-card {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 12px;
      margin: 12px 0;
      page-break-inside: avoid;
    }

    .badge {
      display: inline-block;
      font-size: 8pt;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 4px;
      background: #e2e8f0;
      color: #334155;
    }

    .badge-primary { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }
    .badge-success { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
    .badge-warning { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }

    .page-break {
      page-break-before: always;
    }
  </style>
</head>
<body>

  <!-- Header Cover -->
  <div class="doc-header">
    <div class="doc-badge">Complete Technical Architecture Guide</div>
    <div class="doc-title">Project Manager (AgentPM)</div>
    <div class="doc-subtitle">From Scratch to Advanced: Full-Stack Architecture, Autonomous AI Chatbot ("Jaydip Chatbot"), Tool Calling, Database Schemas, Reactive HTMX Frontend, and Core Terminology</div>
    <div class="doc-meta">
      <div class="doc-meta-item"><strong>Framework:</strong> Django 5.1</div>
      <div class="doc-meta-item"><strong>AI Model:</strong> Google Gemini (via OpenAI SDK)</div>
      <div class="doc-meta-item"><strong>Database:</strong> SQLite3 via Django ORM</div>
      <div class="doc-meta-item"><strong>Frontend:</strong> Tailwind CSS + HTMX 1.9.10</div>
    </div>
  </div>

  <!-- SECTION 1 -->
  <h1>1. Executive Overview & System Purpose</h1>
  <p>
    <strong>Project Manager (AgentPM)</strong> is a multi-tenant project and task execution platform. Traditional project trackers (like Jira or Trello) require manual clicks, complex form submissions, and cumbersome page reloads. 
  </p>
  <p>
    This project bridges traditional project dashboards with an <strong>autonomous AI Copilot ("Jaydip Chatbot")</strong>. Users can interact in two seamless ways:
  </p>
  <ul>
    <li><strong>Traditional Graphical Workspace:</strong> Visual project boards with real-time completion progress meters, high-priority urgent focus queues, and quick inline task creator forms.</li>
    <li><strong>Natural Conversational AI Interface:</strong> A conversational drawer where users issue commands in plain English (e.g. <em>"Plan my mobile app release with 4 milestone tasks"</em>, <em>"Assign the wireframe task to Sarah"</em>, or <em>"What tasks are due soon?"</em>).</li>
  </ul>
  <p>
    When the AI executes an action, it modifies the backend SQLite database in real-time, which emits an event signal that automatically reloads the UI without a full page refresh.
  </p>

  <!-- SECTION 2 -->
  <h1>2. Complete Technology Stack</h1>
  <table>
    <thead>
      <tr>
        <th style="width: 22%;">Technology</th>
        <th style="width: 24%;">Role in Stack</th>
        <th>Technical Rationale & How It Operates</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Python 3 & Django 5.1</strong></td>
        <td>Core Web Framework & Application Server</td>
        <td>Implements the Model-View-Template (MVT) pattern. Handles user authentication, session security, database transactions, request routing, and partial HTML template rendering.</td>
      </tr>
      <tr>
        <td><strong>SQLite 3 (`db.sqlite3`)</strong></td>
        <td>Relational Database Engine</td>
        <td>Zero-configuration, serverless, file-based relational database. Managed strictly via Django's Object-Relational Mapper (ORM), guaranteeing ACID transactional integrity.</td>
      </tr>
      <tr>
        <td><strong>Google Gemini API</strong><br><span class="badge badge-primary">gemini-3.6-flash</span></td>
        <td>Large Language Model (LLM) Engine</td>
        <td>Provides multi-turn reasoning and autonomous function calling. Accessed through the OpenAI-compatible REST endpoint (<code>generativelanguage.googleapis.com/v1beta/openai/</code>) with fallback support.</td>
      </tr>
      <tr>
        <td><strong>HTMX 1.9.10</strong></td>
        <td>Reactive AJAX Frontend Engine</td>
        <td>Enables seamless DOM swapping, event-driven re-rendering (via <code>HX-Trigger</code> headers), and live typing states without bulky SPA frameworks like React or Angular.</td>
      </tr>
      <tr>
        <td><strong>Tailwind CSS</strong></td>
        <td>User Interface Styling</td>
        <td>Utility-first CSS delivering a modern dark-mode aesthetic (slate-950 backdrop, cyan/sky accents, glassmorphic blurred panels, and responsive grid layouts).</td>
      </tr>
      <tr>
        <td><strong>Marked.js</strong></td>
        <td>Markdown Rendering</td>
        <td>Parses raw markdown from AI assistant responses (bullet lists, bold highlights, code formatting) into safe, styled HTML inside the chat bubbles.</td>
      </tr>
    </tbody>
  </table>

  <div class="page-break"></div>

  <!-- SECTION 3 -->
  <h1>3. Database Architecture & Schema Deep-Dive</h1>
  <p>
    The database is structured around four primary models defined in <code>projects/models.py</code>. Multi-tenancy is enforced at the database level: every entity links directly or indirectly to the authenticated Django <code>User</code>.
  </p>

  <h3>Entity Relationship Diagram (ERD)</h3>
  <pre><code>+-----------------------------------------------------------------------------------+
|                                 AUTH_USER (Django)                                |
|  - id (PK)                                                                        |
|  - username (varchar)                                                             |
|  - password (hashed string)                                                       |
+-------------------------+-----------------------------------+---------------------+
                          | 1                                 | 1
                          |                                   |
                          | N (CASCADE)                       | N (CASCADE)
+-------------------------v-------------------+   +-----------v---------------------+
|                  PROJECT                    |   |               CHATMESSAGE       |
|  - id (PK)                                  |   |  - id (PK)                      |
|  - user_id (FK -> User)                     |   |  - user_id (FK -> User)         |
|  - title (CharField: 255)                  |   |  - role (user/assistant/tool)   |
|  - description (TextField)                  |   |  - content (TextField)          |
|  - status (BACKLOG/IN_PROGRESS/COMPLETED)   |   |  - tool_calls (JSONField)       |
|  - created_at, updated_at (DateTime)        |   |  - tool_call_id (CharField)     |
+-------------------------+-------------------+   |  - created_at (DateTime)        |
                          | 1                     +---------------------------------+
                          |
                          | N (CASCADE)
+-------------------------v-------------------+
|                    TASK                     |
|  - id (PK)                                  |
|  - project_id (FK -> Project)               |
|  - title (CharField: 255)                  |
|  - description (TextField)                  |
|  - due_date (DateField, nullable)           |
|  - priority (LOW / MEDIUM / HIGH)           |
|  - assigned_to (CharField: 255)             |
|  - is_completed (BooleanField, default=F)   |
|  - created_at (DateTime)                    |
+---------------------------------------------+</code></pre>

  <h3>Model Attributes & Business Logic</h3>
  <table>
    <thead>
      <tr>
        <th style="width: 20%;">Model</th>
        <th style="width: 25%;">Field / Method</th>
        <th>Purpose & Technical Implementation</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td rowspan="3"><strong>Project</strong></td>
        <td><code>user</code> (ForeignKey)</td>
        <td>Points to Django's <code>User</code>. If the user account is deleted, all their projects are erased via <code>CASCADE</code>.</td>
      </tr>
      <tr>
        <td><code>completion_percentage</code></td>
        <td>Dynamic property: computes <code>(completed_tasks / total_tasks) * 100</code>. Used directly by templates to draw progress bars.</td>
      </tr>
      <tr>
        <td><code>Meta.indexes</code></td>
        <td>B-Tree composite indexes on <code>['user', 'status']</code> and <code>['user', '-created_at']</code> for ultra-fast query execution.</td>
      </tr>
      <tr>
        <td rowspan="3"><strong>Task</strong></td>
        <td><code>priority</code></td>
        <td>Enum: <code>LOW</code>, <code>MEDIUM</code>, <code>HIGH</code>. High-priority unfinished tasks are filtered into the top urgent queue.</td>
      </tr>
      <tr>
        <td><code>assigned_to</code></td>
        <td>Stores the team member handle (e.g. <code>@sarah</code>). Can be set manually or via natural language AI tools.</td>
      </tr>
      <tr>
        <td><code>Meta.ordering</code></td>
        <td><code>['is_completed', '-priority', 'due_date']</code> ensures pending, high-priority, soon-due tasks float to the top.</td>
      </tr>
      <tr>
        <td rowspan="2"><strong>ChatMessage</strong></td>
        <td><code>role</code></td>
        <td>Enum choices: <code>user</code>, <code>assistant</code>, <code>system</code>, <code>tool</code> representing the OpenAI conversation schema.</td>
      </tr>
      <tr>
        <td><code>tool_calls</code> (JSON)</td>
        <td>Preserves raw function call payloads returned by the AI for inspection and audit trails.</td>
      </tr>
    </tbody>
  </table>

  <div class="page-break"></div>

  <!-- SECTION 4 -->
  <h1>4. The AI Autonomous Agent ("Jaydip Chatbot")</h1>
  <p>
    The AI system in <code>projects/ai_agent.py</code> is an implementation of the <strong>ReAct (Reasoning + Acting) Agent Pattern</strong> using function calling.
  </p>

  <h3>Step 1: OpenAI SDK Client with Gemini Gateway</h3>
  <pre><code>client = OpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/',
)</code></pre>
  <p>
    By pointing the official OpenAI client library to Google's v1beta OpenAI-compatible endpoint, standard chat completions and function calls work seamlessly with Gemini models.
  </p>

  <h3>Step 2: Resilient Quota Fallback Architecture (`_call_gemini`)</h3>
  <p>
    To prevent user-facing interruptions caused by free-tier rate limits (HTTP 429), the agent employs an automated fallback ladder:
  </p>
  <div class="callout callout-info">
    <strong>Model Fallback Ladder:</strong>
    <code>gemini-3.6-flash</code> &rarr; <code>gemini-3.5-flash</code> &rarr; <code>gemini-flash-latest</code> &rarr; <code>gemini-3.1-flash-lite</code>
  </div>

  <h3>Step 3: Tool Definitions & Function Schemas</h3>
  <p>
    The model is provided with 8 structured JSON tool definitions (<code>TOOL_SCHEMAS</code>) describing what actions are available:
  </p>
  <table>
    <thead>
      <tr>
        <th>Tool Name</th>
        <th>Input Parameters</th>
        <th>What It Does in the Database</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>list_projects</code></td>
        <td>None</td>
        <td>Queries all projects and tasks for the user and serializes them to JSON for the model's reasoning.</td>
      </tr>
      <tr>
        <td><code>create_project</code></td>
        <td><code>title</code>, <code>description</code></td>
        <td>Inserts a new <code>Project</code> record belonging to <code>request.user</code>.</td>
      </tr>
      <tr>
        <td><code>create_task</code></td>
        <td><code>title</code>, <code>project_title</code>, <code>priority</code>, <code>due_date</code>, <code>assigned_to</code></td>
        <td>Resolves the target project, assigns priority, and creates the <code>Task</code> record. Auto-creates "General Tasks" project if needed.</td>
      </tr>
      <tr>
        <td><code>assign_task</code></td>
        <td><code>task_identifier</code>, <code>project_identifier</code>, <code>assigned_to</code></td>
        <td>Updates task assignee or transfers task between different projects.</td>
      </tr>
      <tr>
        <td><code>update_task_status</code></td>
        <td><code>task_identifier</code>, <code>is_completed</code></td>
        <td>Marks a task completed or pending by name or numeric ID.</td>
      </tr>
      <tr>
        <td><code>delete_task</code></td>
        <td><code>task_identifier</code></td>
        <td>Removes the matching task from the database.</td>
      </tr>
      <tr>
        <td><code>delete_project</code></td>
        <td><code>title</code> or <code>project_id</code></td>
        <td>Deletes the project and cascades deletion to all contained tasks.</td>
      </tr>
    </tbody>
  </table>

  <h3>Step 4: Flexible Entity Resolution Helpers</h3>
  <p>
    Users often refer to tasks colloquially (e.g. <em>"Delete wireframe"</em> instead of <em>"Delete task ID 12"</em>). Helper functions resolve targets intelligently:
  </p>
  <ul>
    <li>Checks if input is a numeric ID (e.g. <code>"5"</code> &rarr; ID match).</li>
    <li>Performs exact case-insensitive match (<code>title__iexact=query</code>).</li>
    <li>Performs substring match (<code>title__icontains=query</code>).</li>
    <li>Falls back to the user's sole project if only one exists.</li>
  </ul>

  <div class="page-break"></div>

  <h3>Step 5: The Multi-Turn ReAct Agent Execution Loop</h3>
  <div class="flow-card">
    <ol style="margin: 0; padding-left: 20px; font-size: 9.5pt;">
      <li><strong>Record User Turn:</strong> Creates a <code>ChatMessage(role='user')</code> in SQLite.</li>
      <li><strong>Assemble History:</strong> Fetches up to 8 recent user/assistant messages to preserve conversational context while minimizing token overhead.</li>
      <li><strong>Inject System Directive:</strong> Injects date, role persona ("Intelligent Project Manager"), markdown formatting instructions, and tool constraints.</li>
      <li><strong>Inference Loop (Max 5 Turns):</strong>
        <ul>
          <li>Calls Gemini API with payload and tools.</li>
          <li>If the response contains <strong>tool_calls</strong>:
            <br>&bull; Iterates each requested tool.
            <br>&bull; Executes matching Python function in <code>AVAILABLE_TOOLS</code> scoped to <code>user</code>.
            <br>&bull; Sets <code>did_mutate = True</code> if data was changed.
            <br>&bull; Appends tool result to the conversation with <code>role: 'tool'</code>.
            <br>&bull; Loops back to Gemini with the tool outputs.
          </li>
          <li>If the response contains text without tool calls:
            <br>&bull; Saves final assistant reply in <code>ChatMessage</code>.
            <br>&bull; Returns <code>(final_reply, did_mutate)</code> to the Django view.
          </li>
        </ul>
      </li>
    </ol>
  </div>

  <!-- SECTION 5 -->
  <h1>5. Reactive Frontend & HTMX Event Synchronization</h1>
  <p>
    Traditional applications either reload the entire browser page or require complex frontend state management (Redux, Vuex). AgentPM achieves full reactivity using <strong>Django + HTMX</strong>:
  </p>

  <h3>The `HX-Trigger: projectStateChanged` Pattern</h3>
  <div class="flow-card">
    <p><strong>1. Chat View Emits Event:</strong> When the AI performs any mutation, <code>views.send_chat</code> attaches an HTTP response header:</p>
    <pre><code>if did_mutate:
    response['HX-Trigger'] = 'projectStateChanged'</code></pre>

    <p><strong>2. Browser Listens & Auto-Updates:</strong> The HTML containers listen for this custom event on the document body:</p>
    <pre><code>&lt;!-- Project Board Container in templates/dashboard.html --&gt;
&lt;div id="project-board" 
     hx-get="{% url 'project_board_partial' %}" 
     hx-trigger="projectStateChanged from:body"&gt;
  {% include "partials/project_board.html" %}
&lt;/div&gt;</code></pre>

    <p><strong>3. Instant Visual Sync:</strong> When Gemini creates a task in the background, HTMX silently fires an AJAX GET request, Django returns the re-rendered <code>project_board.html</code> fragment, and HTMX replaces the inner HTML instantly. The user sees their new project cards and progress bars appear without touching refresh!</p>
  </div>

  <h3>Chatbot Drawer Windowing Modes</h3>
  <p>
    The AI drawer (<code>#ai-drawer</code>) includes three user-selectable window states implemented via lightweight vanilla JavaScript:
  </p>
  <ul>
    <li><strong>Default Compact View (384px width):</strong> Anchored on the right side of the workspace, allowing simultaneous board view and chatting.</li>
    <li><strong>Maximized / Expanded View (820px width):</strong> Expands across the screen for wide-angle roadmapping, long checklists, and detailed project breakdowns.</li>
    <li><strong>Minimized Floating Mode:</strong> Completely folds away into a bottom-right floating pill button with an animated emerald pulse beacon, freeing 100% of workspace canvas.</li>
  </ul>

  <div class="page-break"></div>

  <!-- SECTION 6 -->
  <h1>6. Project Directory & File Guide</h1>
  <table>
    <thead>
      <tr>
        <th style="width: 30%;">File Path</th>
        <th>Description & Responsibilities</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>core/settings.py</code></td>
        <td>Application configuration: loads environment variables (<code>.env</code>), configures SQLite database, installed apps, middleware, and Gemini API credentials.</td>
      </tr>
      <tr>
        <td><code>core/urls.py</code></td>
        <td>Top-level URL routing table. Mounts Django admin at <code>/admin/</code> and includes <code>projects.urls</code> at the root <code>/</code>.</td>
      </tr>
      <tr>
        <td><code>projects/models.py</code></td>
        <td>Defines <code>Project</code>, <code>Task</code>, and <code>ChatMessage</code> ORM tables, relationships, cascade behaviors, and indexes.</td>
      </tr>
      <tr>
        <td><code>projects/ai_agent.py</code></td>
        <td>The autonomous bot engine. Contains OpenAI-Gemini client, fallback handler, tool functions, schemas, and ReAct loop.</td>
      </tr>
      <tr>
        <td><code>projects/views.py</code></td>
        <td>Controllers for user registration, workspace dashboard, HTMX action handlers (create/toggle/delete tasks), and <code>send_chat</code>.</td>
      </tr>
      <tr>
        <td><code>projects/urls.py</code></td>
        <td>URL routing for dashboard, login/logout, task toggles, and chat API endpoints.</td>
      </tr>
      <tr>
        <td><code>templates/base.html</code></td>
        <td>Master HTML5 layout. Loads Tailwind CDN, HTMX CDN, Marked.js, and configures global CSRF headers on HTMX requests.</td>
      </tr>
      <tr>
        <td><code>templates/dashboard.html</code></td>
        <td>Main workspace interface: top navigation, urgent tasks, project boards, add task/project modals, and the AI chatbot drawer.</td>
      </tr>
      <tr>
        <td><code>templates/partials/*.html</code></td>
        <td>Modular HTML fragments (<code>project_board.html</code>, <code>task_item.html</code>, <code>urgent_tasks.html</code>, <code>chat_stream.html</code>) swapped by HTMX.</td>
      </tr>
    </tbody>
  </table>

  <!-- SECTION 7 -->
  <h1>7. Glossary of Key Terms</h1>
  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Term</th>
        <th>Definition & Context in this Project</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>ORM (Object-Relational Mapping)</strong></td>
        <td>A programming technique that maps database tables to Python classes. Allows developers to interact with the database using Python objects (<code>Task.objects.create(...)</code>) rather than writing raw SQL.</td>
      </tr>
      <tr>
        <td><strong>Multi-Tenancy</strong></td>
        <td>An architecture where multiple users share the same system and database, but their records are strictly isolated. In AgentPM, every database operation verifies <code>user=request.user</code>.</td>
      </tr>
      <tr>
        <td><strong>Foreign Key & CASCADE</strong></td>
        <td>A relational link between tables. <code>CASCADE</code> ensures that if a parent record is deleted (e.g. a Project), all child records (Tasks) are automatically purged to prevent orphan data.</td>
      </tr>
      <tr>
        <td><strong>Function / Tool Calling</strong></td>
        <td>A capability where the LLM does not just reply with text, but emits a structured JSON object specifying a function name and arguments to execute programmatic changes.</td>
      </tr>
      <tr>
        <td><strong>ReAct Pattern</strong></td>
        <td>"Reasoning + Acting". A design pattern where an AI alternates between thinking, executing external tools, observing the output, and arriving at a conclusive user response.</td>
      </tr>
      <tr>
        <td><strong>HTMX Partial Swapping</strong></td>
        <td>The technique of returning small chunks of server-rendered HTML from the backend and inserting them directly into specified DOM elements without redrawing the whole page.</td>
      </tr>
      <tr>
        <td><strong>CSRF Protection</strong></td>
        <td>Cross-Site Request Forgery mitigation. Django injects a cryptographically signed token into forms, verified on every state-mutating POST request.</td>
      </tr>
      <tr>
        <td><strong>Database Indexing</strong></td>
        <td>Data structures created on specific database columns (e.g. <code>user</code>, <code>status</code>) allowing the database engine to locate records in $O(\log n)$ time rather than full table scans.</td>
      </tr>
    </tbody>
  </table>

  <div class="callout callout-success" style="margin-top: 20px;">
    <strong>Architecture Complete</strong>
    This document serves as the exhaustive reference manual for the AgentPM system architecture, database schema, AI engine, and interactive frontend.
  </div>

</body>
</html>
"""

temp_html_path = Path("c:/Users/l/OneDrive/Desktop/project_manager/documentation.html")
temp_pdf_path = Path("c:/Users/l/OneDrive/Desktop/project_manager/Project_Manager_Full_Documentation.pdf")

temp_html_path.write_text(html_content, encoding="utf-8")
print(f"HTML saved to {temp_html_path}")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={temp_pdf_path}",
    "--no-pdf-header-footer",
    str(temp_html_path.resolve())
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
print("PDF created:", temp_pdf_path.exists())
if temp_pdf_path.exists():
    print("PDF File Size:", temp_pdf_path.stat().st_size, "bytes")

