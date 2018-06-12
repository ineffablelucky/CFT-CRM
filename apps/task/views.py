from django.shortcuts import render
from .models import Task

def project_manager_task_index(request):
    task = Task.objects.all()
    context = {
        'task': task
    }
    return render(request, 'manager_task_page.html', context)

def employee_task_index(request):
    task = Task.objects.all()
    context = {
        'task': task
    }
    return render(request, 'employee_task_page.html', context)
