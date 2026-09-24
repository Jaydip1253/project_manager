from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Profile & Password
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),

    # HTMX Partials & Actions
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/toggle/', views.toggle_task, name='toggle_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('projects/create/', views.create_project, name='create_project'),
    path('partials/projects/', views.project_board_partial, name='project_board_partial'),
    path('partials/urgent-tasks/', views.urgent_tasks_partial, name='urgent_tasks_partial'),
    path('api/chat/', views.send_chat, name='send_chat'),
    path('api/chat/clear/', views.clear_chat, name='clear_chat'),
]