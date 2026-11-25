from django.contrib import admin

from .models import ActivityLog, Board, Column, Comment, Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'column', 'assignee', 'priority', 'due_date')
    list_filter = ('priority', 'due_date')
    search_fields = ('title',)


admin.site.register(Board)
admin.site.register(Column)
admin.site.register(Comment)
admin.site.register(ActivityLog)