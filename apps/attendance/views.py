from django.shortcuts import render
from .forms import LeaveForm, AttendanceForm
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.http import HttpResponseForbidden, HttpResponse
from ..leave.models import Leave
from ..attendance.models import Attendance, LeaveRequest
from ..attendance.models import LeaveRequest
from django.db.models import Q
from ..users.models import MyUser


import datetime
from copy import deepcopy


class LeaveRequestView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
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
        context = super(LeaveRequestView, self).get_context_data(**kwargs)
        context["leave"] = Leave.objects.get(user_id=self.request.user)
        context["list_leave_request"] = LeaveRequest.objects.filter(user_id=self.request.user)
        return context

    def form_valid(self, form):
        ins = form.save()
        # for i in ins:
        #     print(i.id)
        return redirect('/attendance/leave')




"""
class ShowingLeaveRequest(LoginRequiredMixin, ListView):
    template_name = 'leaverequest.html'
    model = Leave
    context_object_name = 'showrequest'

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
            elif a.time_in.hour > 18 and a.time_in.minute >30:
                a.status = 'absent'
            else:
                delta = datetime.timedelta(hours=9, minutes=30)
                late = a.time_in - delta
                a.note = str(late.hour)+" hrs" + str(late.minute) + " min's Late"

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
    permission_required = ('users.view_users', 'attendance.view_attendance')
    template_name = 'attendance/showattendance.html'
    model = Attendance
    context_object_name = 'attendance'

    def get_queryset(self):
        temp = MyUser.objects.all()

        if datetime.date.today().weekday() == 0:
            delta = datetime.timedelta(days=3)
        elif datetime.date.today().weekday() == 6:
            delta = datetime.timedelta(days=2)
        else:
            delta = datetime.timedelta(days=1)
        p = []
        for t in temp:
            p.append(t.pk)
        temp2 = Attendance.objects.filter(date=datetime.date.today()-delta)
        for t in temp2:
            if t.status == 'absent':
                if LeaveRequest.objects.filter(Q(user_id=t.user_id) & Q(date__gte=datetime.date.today() - delta)
                                        & Q(end_date__lte=datetime.date.today()-delta)
                                        & Q(status='Approved')):
                    t.status = 'On Lea'
                    t.save()

        l = []
        for t in temp2:
            tt = MyUser.objects.get(id=t.user_id)
            l.append(tt.pk)

        p = [x for x in p if x not in l]
        for i in range(len(p)):
            absent = Attendance.objects.create(user_id=p[i], date=datetime.date.today()-delta,
                                               status='absent')
            # if LeaveRequest.objects.get(Q(user_id=p[i]) & Q(date__gte=datetime.date.today()-delta)
            #                             & Q(end_date__lte=datetime.date.today()-delta)
            #                             & Q(status='Approved')):
            #     absent.status = 'On Leave'
            absent.save()
        date = self.request.GET.get('date', None)
        if datetime.date.today().weekday() == 0:
            queryset = Attendance.objects.filter(date=datetime.date.today()-datetime.timedelta(days=3))
        else:
            queryset = Attendance.objects.filter(date=datetime.date.today() - datetime.timedelta(days=1))
        if date is not None:
            queryset = Attendance.objects.filter(date=date)
        return queryset.order_by('user_id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = AttendanceForm()
        return context


class EmployAttendance(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('users.view_users', 'attendance.view_attendance')
    template_name = 'attendance/employattendance.html'
    model = Attendance
    context_object_name = 'attendance'

    def get_queryset(self):
        queryset = Attendance.objects.filter(user_id=self.kwargs.get('id'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['employee'] = MyUser.objects.get(id=self.kwargs.get('id'))
        abc = Attendance.objects.filter(user_id=self.kwargs.get('id'))
        working_hours = []
        context['ab']=[]
        tmp = []
        for a in abc:
            if a.time_out is None:
                wh = 0
                s = str(wh)
                working_hours.append(s)

            elif a.status is 'absent':
                wh = 0
                s = str(wh)
                working_hours.append(s)

            else:
                delta = datetime.timedelta(hours=a.time_in.hour, minutes=a.time_in.minute)
                wh = a.time_out-delta
                s = str(wh.hour)+" hrs " + str(wh.minute) + " min's"
                working_hours.append(s)
            a.working_hours = s
            tmp.append(a)

        context['o'] = tmp

        return context



"""
class ShowAbsentEmployee(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('users.view_attendance',)
    template_name = 'attendance/showattendance.html'
    model = Attendance
    context_object_name = 'absent'

    def get_queryset(self):
        queryset = Attendance.objects.filter(date=datetime.date.today())
        queryset2 = MyUser.objects.filter(~Q())
"""