from django.shortcuts import render, HttpResponseRedirect
from .models import IT_Project
from django.views.generic import TemplateView
from .forms import CreateProjectForm
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

def create_project_form(request):

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():

            form.save()
            return HttpResponseRedirect('/')
    else:
        form = CreateProjectForm()

    return render(request, 'create_project_form.html', {'form': form})
