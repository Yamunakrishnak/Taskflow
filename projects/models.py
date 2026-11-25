from django.conf import settings
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Board(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='boards')
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.project.name} / {self.name}'


class Column(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=60)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.board.name} / {self.name}'


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks',
    )
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    due_date = models.DateField(null=True, blank=True)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author} on {self.task}'


class ActivityLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activity')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.action