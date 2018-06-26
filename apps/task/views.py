
from .models import Task, Time_Entry
from django.views.generic import TemplateView, ListView
from .forms import CreateTaskForm
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from apps.users.models import MyUser
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from apps.project.models import IT_Project
from datetime import datetime
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import redirect


class TaskList(LoginRequiredMixin,  ListView):
    model = Task
    context_object_name = 'task_list'
    permission_required = ('users.view_task',)

    def get_queryset(self):
        queryset = Task.objects.filter(project__id=self.kwargs.get('pk'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs.get('pk')

        return context


class Employee_Task_List(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('task.view_task',)
    model = Task
    context_object_name = 'emp_task_list'
    template_name = "my tasks.html"

    def get_queryset(self):
        temp = Task.objects.filter(employee_id=self.request.user)

        return temp


class TaskCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = ('task.add_task')
    form_class = CreateTaskForm
    template_name = "create_task_form.html"
    success_url = '/project'

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     print(self.kwargs)
    #     kwargs.update({'project_id': self.kwargs.get('pk')})
    #
    #     return kwargs

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['project_id'] = self.kwargs.get('pk')
    #
    #     return context


class Edit_Task(LoginRequiredMixin, UpdateView):
    form_class = CreateTaskForm
    template_name = "create_task_form.html"
    success_url = '/task'


class Details_Task(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task_list'
    template_name = "task_details.html"
#
# class Start_Task(LoginRequiredMixin, CreateView):

def entry(request, pk):
        print("helloooooooooooooooooooooooooooooo")

        if not request.user.is_authenticated:
            return HttpResponseForbidden
        # elif Time_Entry.objects.filter(task_start_date_time=datetime.today()):
        #     return HttpResponse("Task Already started! You can start working")
        else:
            tas = Task.objects.get(pk=pk)
            a = Time_Entry.objects.create(task=tas,
                                      task_start_date_time=datetime.today(),
                                      )
            print(tas)
            tas.task_current_state = 'running'
            print("printing tas. task curent state", tas.task_current_state)

            tas.save()
            a.save()
            # b.save()
            # print(b.task_current_state)

            return redirect(reverse('task:task-details', kwargs={'pk' : tas.id}))




def end(request, pk):
        print("byeeeeeeeeeeeeeeeeeeeeeeee")
        if not request.user.is_authenticated:
            return HttpResponseForbidden
        else:
            tas = Task.objects.get(pk=pk)

            b = Time_Entry.objects.create(
                                      task = tas,
                                      task_end_date_time=datetime.today(),
                                      )

            tas.task_current_state = 'stopped'
            tas.save()
            b.save()

            return redirect(reverse('task:task-details', kwargs= {'pk' : tas.id}))
