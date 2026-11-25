from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectForm
from .models import ActivityLog, Board, Column, Project, Task
from django.db.models import Prefetch

DEFAULT_COLUMNS = ['To Do', 'In Progress', 'Done']


@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            board = Board.objects.create(project=project, name='Main board')
            Column.objects.bulk_create([
                Column(board=board, name=name, position=index)
                for index, name in enumerate(DEFAULT_COLUMNS)
            ])
            ActivityLog.objects.create(
                project=project,
                actor=request.user,
                action=f'Created project "{project.name}"',
            )
        return redirect('project_detail', pk=project.pk)
    return render(request, 'projects/project_form.html', {'form': form})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    board = project.boards.first()
    columns = []
    if board:
        tasks = Task.objects.select_related('assignee')
        columns = board.columns.prefetch_related(Prefetch('tasks', queryset=tasks))
    activity = project.activity.select_related('actor')[:10]
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'board': board,
        'columns': columns,
        'activity': activity,
    })