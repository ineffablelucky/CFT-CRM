from django.shortcuts import render
from .forms import LeaveForm
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.http import HttpResponseForbidden, HttpResponse
from ..leave.models import Leave
from ..attendance.models import Attendance
from django.db.models import Q


import datetime
from copy import deepcopy


class LeaveRequest(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('attendance.add_leaverequest',)
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

    def get_context_data(self, **kwargs):
        context = super(LeaveRequest, self).get_context_data(**kwargs)
        context["leave"] = Leave.objects.get(user_id=self.request.user)
        return context

    def form_valid(self, form):
        ins = form.save()
        # for i in ins:
        #     print(i.id)
        return HttpResponse("Request Send")




"""
class LeaveTable(LoginRequiredMixin, ListView):
    template_name = 'leaverequest.html'
    model = Leave
    context_object_name = 'leave'

    def get_queryset(self):
        queryset = Leave.objects.get(user_id = self.request.user.id)
        return queryset
"""


class Completed(LoginRequiredMixin, TemplateView):
    template_name = 'complete.html'


class Clock(LoginRequiredMixin,TemplateView):
    template_name = 'clock_in.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'clock_in.html')


class Clockin(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('attendance.add_attendance',)
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
            if a.time_in.hour <= 9 and a.time_in.minute <= 30:
                a.note = "On Time"
            else:
                hour_late = a.time_in.hour - 9
                min_late = a.time_in.hour-30
                a.note = str(hour_late)+" hrs" + str(min_late) + " mins Late"

            a.save()
            return redirect('/attendance/userattendance')


class Clockout(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'clock_in.html'
    permission_required = ('attendance.add_attendance',)

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseForbidden

        else:
            a = Attendance.objects.get(user_id = self.request.user, date=datetime.date.today())
            if a is None:
                return HttpResponse("first CLock In")
            elif a.time_out is not None:
                return HttpResponse("Clockout Done")
            else:
                a.time_out = datetime.datetime.today()
                a.save()
            return redirect('/attendance/userattendance')


class PastAttendance(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('attendance.view_attendance',)
    template_name = 'clock_in.html'
    model = Attendance
    context_object_name = 'attendance'

    def get_queryset(self):
        delta = datetime.timedelta(days=3)
        queryset = Attendance.objects.filter(Q(user_id=self.request.user) & Q(date__lte=datetime.date.today())
                                             & Q(date__gte=datetime.date.today()-delta))
        return queryset


class ShowAttendance(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('users.view_attendance',)
    template_name = 'attendance/showattendance.html'
    model = Attendance
    context_object_name = 'attendance'

    def get_queryset(self):
        queryset = Attendance.objects.filter(date=datetime.date.today())
        return queryset
