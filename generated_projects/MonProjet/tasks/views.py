from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages #Added for flash messages

def task_list(request):
    tasks = Task.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(tasks, 10)

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    return render(request, 'tasks/task_list.html', {'tasks': tasks})


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully!') #Flash message
            return redirect('task_list')
        else:
            messages.error(request, 'Invalid form submission.') #Flash message

    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!') #Flash message
            return redirect('task_list')
        else:
            messages.error(request, 'Invalid form submission.') #Flash message
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        try:
            task.delete()
            messages.success(request, 'Task deleted successfully!') #Flash message
            return redirect('task_list')
        except Exception as e:
            messages.error(request, f'Error deleting task: {e}') #Flash message
            return redirect('task_list') # Redirect back to list on error
    return render(request, 'tasks/task_delete.html', {'task': task})



