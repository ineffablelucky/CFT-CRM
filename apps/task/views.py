from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .models import Task
from django.views.generic import TemplateView, ListView
from .forms import CreateTaskForm
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from apps.users.models import MyUser
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from apps.project.models import IT_Project

class TaskList(LoginRequiredMixin,  ListView):
    model = Task
    context_object_name = 'task_list'
    permission_required = ('users.view_task',)

    def get_queryset(self):
        queryset = Task.objects.filter(project__id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs.get('pk')

        return context


class Employee_Task_List(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('task.view_task',)
    model = Task
    context_object_name = 'emp_task_list'
    template_name = "my tasks.html"

    def get_queryset(self):
        temp = Task.objects.filter(employee_id=self.request.user)
        print(temp)
        return temp


class TaskCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = ('task.add_task')
    form_class = CreateTaskForm
    template_name = "create_task_form.html"
    success_url = '/project'

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'project_id': self.kwargs.get('pk')})
    #
    #     return kwargs

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['project_id'] = self.kwargs.get('pk')
    #
    #     return context


class Edit_Task(LoginRequiredMixin, UpdateView):
    form_class = CreateTaskForm
    template_name = "create_task_form.html"
    success_url = '/task'


class Details_Task(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task_list'
    template_name = "task_details.html"

