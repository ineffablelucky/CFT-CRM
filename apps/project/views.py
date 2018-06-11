from django.shortcuts import render
from .models import IT_Project
from django.views.generic import TemplateView

#class AboutView(TemplateView):
 #   template_name = "project_manager_view"

def project_manager_index(request):
    project = IT_Project.objects.all()
    context = {
        'project': project
    }
    return render(request, 'project_manager_view.html', context)

def employee_project(request):
    project = IT_Project.objects.all()
    context = {
        'project': project
    }
    return render(request, 'employee_view.html', context)

