from django.shortcuts import render
from .models import Module
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from apps.project.models import IT_Project

# def module_index(request):
#     module = Module.objects.all()
#     context = {
#         'module': module
#     }
#     return render(request, 'project_module.html', context)
class Details_Project(DetailView):
    model = IT_Project
    template_name = "project_view.html"

class ListModule(ListView):
    model = Module
    template_name = "project_view.html"

    queryset = Module.objects.order_by('module_name')
    context_object_name = 'modules'

