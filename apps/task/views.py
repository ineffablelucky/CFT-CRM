from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .models import Task
from django.views.generic import TemplateView, ListView
from .forms import CreateTaskForm
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

class TaskList(ListView):
    model = Task
    context_object_name = 'task_list'

    # def get_queryset(self):
    #     self.task = get_object_or_404(Task, name=self.kwargs['task'])
    #     return Task.objects.filter(task=self.task)

class Employee_Task_List(ListView):
    model = Task

class TaskCreate(CreateView):
    form_class = CreateTaskForm
    template_name = "add_task.html"
    success_url = '/task'

class Edit_Task(UpdateView):
    form_class = CreateTaskForm
    template_name = "add_task.html"
    success_url = '/task'

class Details_Task(DetailView):
    model = Task
    context_object_name = 'task_list1'
    template_name = "task_view.html"

