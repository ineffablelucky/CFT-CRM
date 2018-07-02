from django.shortcuts import render, HttpResponseRedirect
from .models import IT_Project
from apps.opportunity.models import Opportunity
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .forms import CreateProjectForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from apps.task.models import Task


#display list of company's created projects
class ProjectList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('project.view_it_project', 'users.view_users',)
    model = IT_Project
    template_name = 'project_manager_list.html'

    def get_queryset(self):
        queryset = IT_Project.objects.filter(opportunity=None)
        # print(queryset)
        return queryset


#display list of opportunities converted into project
class OppProjectList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('project.view_it_project', 'users.view_users',)
    model = IT_Project
    template_name = 'projects.html'

    def get_queryset(self):
        queryset = IT_Project.objects.filter(Q(opportunity__isnull=False) )
        print(queryset)
        # queryset = IT_Project.objects.filter(Q(opportunity is not None) & Q(assigned_to = self.request.user))
        return queryset


#display projects assigned to employee
class Employee_Project_List(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = ('project.view_it_project',)
    model = IT_Project
    template_name = "my projects.html"

    def get_queryset(self):
        temp = IT_Project.objects.filter(employees_per_project=self.request.user)
        #print(temp)
        return temp

#project creation form
class ProjectCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = ('project.add_it_project',)

    form_class = CreateProjectForm
    template_name = 'create_project_form.html'
    success_url = '/project'

#change project form
class Edit_Project(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = ('project.change_it_project',)
    model = IT_Project
    form_class = CreateProjectForm
    template_name = "create_project_form.html"
    success_url = '/project'

#show modules of projects
class ListModule(LoginRequiredMixin, DetailView):
    model = IT_Project
    template_name = "project_details.html"

#show no of tasks completed and total no of tasks
def proj_progress(request, pk):
    pass
    a = Task.objects.filter(project_id = pk)

