from django.shortcuts import render, HttpResponseRedirect
from .models import IT_Project
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .forms import CreateProjectForm

class ProjectList(ListView):
    model = IT_Project

class Employee_Project_List(ListView):
    model = IT_Project
    template_name = "my projects.html"

    def get_queryset(self):
        temp = IT_Project.objects.filter(employees_per_project=self.request.user)
        print(temp)
        return temp


class ProjectCreate(CreateView):
    form_class = CreateProjectForm
    template_name = 'create_project_form.html'
    success_url = '/project'

class Edit_Project(UpdateView):
    model = IT_Project
    form_class = CreateProjectForm
    template_name = "create_project_form.html"
    success_url = '/project'

class ListModule(DetailView):
    model = IT_Project
    template_name = "project_details.html"


