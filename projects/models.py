from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    class Status(models.TextChoices):
        BACKLOG = 'BACKLOG', 'Backlog'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BACKLOG)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return self.title

    @property
    def completion_percentage(self):
        total = self.tasks.count()
        if total == 0:
            return 0
        completed = self.tasks.filter(is_completed=True).count()
        return int((completed / total) * 100)


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    assigned_to = models.CharField(max_length=255, blank=True, default='')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['is_completed', '-priority', 'due_date']
        indexes = [
            models.Index(fields=['project', 'is_completed']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        return f"{self.title} ({'Done' if self.is_completed else 'Pending'})"


class ChatMessage(models.Model):
    class Role(models.TextChoices):
        USER = 'user', 'User'
        ASSISTANT = 'assistant', 'Assistant'
        SYSTEM = 'system', 'System'
        TOOL = 'tool', 'Tool'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_history')
    role = models.CharField(max_length=15, choices=Role.choices)
    content = models.TextField(blank=True, default='')
    tool_calls = models.JSONField(null=True, blank=True)
    tool_call_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]