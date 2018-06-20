from django.shortcuts import render, HttpResponseRedirect
from .models import IT_Project
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import CreateProjectForm
from django.views.generic.edit import FormView
import json
from django.http import HttpResponse
from django.urls import reverse_lazy
from ..module.models import Module


class ProjectList(ListView):
    model = IT_Project



class Employee_Project_List(ListView):
    model = IT_Project

class ProjectCreate(CreateView):
    #model = IT_Project
    form_class = CreateProjectForm
    template_name = 'create_project_form.html'
    success_url = '/project'

class Edit_Project(UpdateView):
    model = IT_Project
    form_class = CreateProjectForm
    template_name = "create_project_form.html"
    success_url = '/project'

class Details_Project(DetailView):
    model = IT_Project
    template_name = "project_view.html"









#     def form_valid(self, form):
#         form.save()
#
#     def get_success_url(self, **kwargs):
#         return reverse_lazy('project:manager-project-view')
#
# class Project_Delete(DeleteView):
#     model = IT_Project