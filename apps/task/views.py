from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .models import Task
from django.views.generic import TemplateView, ListView
from .forms import CreateTaskForm
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from apps.users.models import MyUser
from apps.project.models import IT_Project
class TaskList(ListView):
    model = Task
    context_object_name = 'task_list'

    def get_queryset(self):
        queryset = Task.objects.filter(project__id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs.get('pk')
        print("5555555555555555555555555")
        print(context)
        return context


class Employee_Task_List(ListView):
    model = Task

    context_object_name = 'emp_task_list'

    def get_queryset(self):
        queryset = Task.objects.filter(project__id=self.kwargs.get('pk'))
        return queryset


class TaskCreate(CreateView):
    form_class = CreateTaskForm
    template_name = "create_task_form.html"
    success_url = '/task/1'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'project_id': self.kwargs.get('pk')})
        print('*******************')
        print(kwargs)
        return kwargs


class Edit_Task(UpdateView):
    form_class = CreateTaskForm
    template_name = "create_task_form.html"
    success_url = '/task'


class Details_Task(DetailView):
    model = Task
    context_object_name = 'task_list'
    template_name = "task_details.html"

