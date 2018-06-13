from django.shortcuts import render, HttpResponseRedirect
from .models import Task
from django.views.generic import TemplateView, ListView
from .forms import CreateTaskForm
from django.views.generic.edit import FormView


class TaskList(ListView):
    model = Task
    context_object_name = 'task_list'

class Employee_Task_List(ListView):
    model = Task

class TaskCreate(FormView):
    model = Task
    form_class = CreateTaskForm

    def form_valid(self, form):
        form.save()
