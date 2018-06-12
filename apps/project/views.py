from django.shortcuts import render, HttpResponseRedirect
from .models import IT_Project
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .forms import CreateProjectForm
from django.views.generic.edit import FormView


class ProjectList(ListView):
    model = IT_Project

class Employee_Project_List(ListView):
    model = IT_Project

class ProjectCreate(CreateView):
    model = IT_Project
    form_class = CreateProjectForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class Edit_Project(UpdateView):
    model = IT_Project
    form_class = CreateProjectForm


    def form_valid(self, form):
        form.save()

class Project_Delete(DeleteView):
    model = IT_Project