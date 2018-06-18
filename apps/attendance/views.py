from django.shortcuts import render
from .forms import LeaveForm
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import HttpResponseForbidden, HttpResponse
from ..leave.models import Leave
from ..attendance.models import Attendance

import datetime
from copy import deepcopy


class LeaveRequest(LoginRequiredMixin, CreateView):
    form_class = LeaveForm
    template_name = 'leaverequest.html'
    success_url = '/'
    model = Leave
    context_object_name = 'leave'

    def get_form_kwargs(self):
        """Returns the keyword arguments for instantiating the form"""
        kwargs = super().get_form_kwargs()
        kwargs.update({'logged_user': self.request.user})
        return kwargs

    # def form_valid(self, form):
    #     data = []
    #     saved_instance = []
    #     tmp_instances = []
    #     start_date = form.cleaned_data.get('date')
    #     end_date = form.cleaned_data.get('end_date')
    #     delta = datetime.timedelta(days=1)
    #     while start_date <= end_date:
    #         data.append(start_date)
    #         start_date += delta
    #     for date in data:
    #         form
    #         tmp = deepcopy(form)
    #         tmp.date = date
    #         tmp_instances.append(tmp)
    #     print(tmp_instances)
    #     for i in tmp_instances:
    #         print(i.date)
    #         obj = i.save()
    #         saved_instance.append(obj)
    #     print(saved_instance)
    #     return redirect('/')

    def form_valid(self, form):
        ins = form.save()
        # for i in ins:
        #     print(i.id)
        return redirect('/')


class Completed(LoginRequiredMixin, TemplateView):
    template_name = 'complete.html'


class Clock(LoginRequiredMixin,TemplateView):
    template_name = 'clock_in.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'clock_in.html')


class Clockin(LoginRequiredMixin, CreateView):
    template_name = 'clock_in.html'
    success_url = '/'
    """
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'logged_user': self.request.user})
        return kwargs
    """
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseForbidden
        elif Attendance.objects.filter(user_id=self.request.user.id, date=datetime.date.today()):
            return HttpResponse("Already Clocked In")

        else:
            a = Attendance.objects.create(user_id=self.request.user.id,
                                      date=datetime.date.today(),
                                      time_in=datetime.datetime.today(),
                                      status='present',
                                      )
            a.save()
            return redirect('/')


class Clockout(LoginRequiredMixin, UpdateView):
    template_name = 'clock_in.html'

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseForbidden

        else:
            a = Attendance.objects.get(user_id = self.request.user, date=datetime.date.today())
            if a is None:
                return HttpResponse("first CLock In")
            else:
                a.time_out = datetime.datetime.today()
                a.save()
            return redirect('/')


