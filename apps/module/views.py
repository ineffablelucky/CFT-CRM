from django.shortcuts import render
from .models import Module

def module_index(request):
    module = Module.objects.all()
    context = {
        'module': module
    }
    return render(request, 'project_module.html', context)