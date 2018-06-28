from django.shortcuts import render, HttpResponseRedirect
from .models import IT_Project
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .forms import CreateProjectForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q

class ProjectList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('users.view_project',)
    model = IT_Project
    def get_queryset(self):
        queryset = IT_Project.objects.all(
        )
        print(queryset)
        return None

class Employee_Project_List(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = ('project.view_project',)
    model = IT_Project
    template_name = "my projects.html"

    def get_queryset(self):
        temp = IT_Project.objects.filter(employees_per_project=self.request.user)
        print(temp)
        return temp


class ProjectCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = ('project.add_it_project',)

    form_class = CreateProjectForm
    template_name = 'create_project_form.html'
    success_url = '/project'

class Edit_Project(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = ('project.change_it_project',)
    model = IT_Project
    form_class = CreateProjectForm
    template_name = "create_project_form.html"
    success_url = '/project'

class ListModule(LoginRequiredMixin, DetailView):
    model = IT_Project
    template_name = "project_details.html"



