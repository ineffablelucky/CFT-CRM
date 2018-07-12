from django.shortcuts import render
from .forms import LeaveForm, AttendanceForm, GraphForm
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.http import HttpResponseForbidden, HttpResponse, StreamingHttpResponse
from ..leave.models import Leave
from ..attendance.models import Attendance, LeaveRequest
from ..attendance.models import LeaveRequest
from django.db.models import Q
from ..users.models import MyUser   
import csv
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict


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
        return JsonResponse({'a': 'True'})
        # return redirect('/attendance/leave/')

    def form_invalid(self, form):
        print(form.errors)
        return JsonResponse({'error': form.errors})




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
            a = "Clocked In"
            return JsonResponse({'a': a})

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
            time_in = str(a.time_in.hour)+":"+str(a.time_in.minute)

            return JsonResponse({'a': time_in})


class Clockout(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'clock_in.html'
    permission_required = ('attendance.add_attendance',)

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseForbidden

        else:
            if Attendance.objects.filter(user_id=self.request.user, date=datetime.date.today()):
                a = Attendance.objects.get(user_id=self.request.user, date=datetime.date.today())
                if a.time_out is not None:
                    return JsonResponse({'b': "Clockout Done"})
                else:
                    a.time_out = datetime.datetime.today()
                    a.save()
                    time_out = str(a.time_out.hour)+":"+str(a.time_out.minute)
                    return JsonResponse({'b': time_out})
            else:
                return JsonResponse({'b': "First Clock In"})


class PastAttendance(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('attendance.view_attendance',)
    template_name = 'users/employee/home.html'
    model = Attendance
    context_object_name = 'attendance'

    def get_queryset(self):
        delta = datetime.timedelta(days=3)
        queryset = Attendance.objects.filter(Q(user_id=self.request.user) & Q(date__lte=datetime.date.today())
                                             & Q(date__gte=datetime.date.today()-delta))
        return queryset


class ShowAttendance(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('attendance.view_attendance', 'attendance.change_attendance')
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
        temp2 = Attendance.objects.filter(date=datetime.date.today() - delta)
        l = []
        for t in temp2:
            tt = MyUser.objects.get(id=t.user_id)
            l.append(tt.pk)

        p = [x for x in p if x not in l]
        for i in range(len(p)):
            if MyUser.objects.filter(Q(id=p[i]) & Q(date_of_joining__lte=datetime.date.today()-delta)):

                absent = Attendance.objects.create(user_id=p[i], date=datetime.date.today()-delta, status='absent')
                leave = Leave.objects.get(user_id=p[i])
                absent.save()
                if leave.pl > 0:
                    leave.pl = leave.pl-1
                    leave.save()
                    absent.note = "PL"
                elif leave.cl > 0:
                    leave.cl = leave.cl-1
                    leave.save()
                    absent.note = "CL"

        for t in temp2:
            if t.status == 'absent':
                if LeaveRequest.objects.filter(Q(user_id=t.user_id) & Q(date__lte=datetime.date.today() - delta)
                                               & Q(end_date__gte=datetime.date.today() - delta)
                                               & Q(status='Approved')):
                    t.status = 'On Leave'
                    t.save()
        from_date = self.request.GET.get('date', None)
        to_date = self.request.GET.get('to_date', None)
        if datetime.date.today().weekday() == 0:
            queryset = Attendance.objects.filter(date=datetime.date.today()-datetime.timedelta(days=3))
        else:
            queryset = Attendance.objects.filter(date=datetime.date.today() - datetime.timedelta(days=1))
        if from_date is not None and to_date is not None:
            queryset = Attendance.objects.filter(Q(date__gte=from_date) & Q(date__lte=to_date))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = AttendanceForm()
        return context


class EmployAttendance(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('attendance.view_attendance', 'attendance.change_attendance')
    template_name = 'attendance/employattendance.html'
    model = Attendance
    context_object_name = 'attendance'

    def get_queryset(self):
        from_date = self.request.GET.get('date', None)
        to_date = self.request.GET.get('to_date', None)
        queryset = Attendance.objects.filter(user_id=self.kwargs.get('id'))
        if from_date is not None and to_date is not None:
            queryset = Attendance.objects.filter(Q(user_id=self.kwargs.get('id')) & Q(date__gte=from_date) & Q(date__lte=to_date))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = AttendanceForm()
        context['employee'] = MyUser.objects.get(id=self.kwargs.get('id'))
        from_date = self.request.GET.get('date', None)
        to_date = self.request.GET.get('to_date', None)
        abc = Attendance.objects.filter(user_id=self.kwargs.get('id'))
        if from_date is not None and to_date is not None:
            abc = Attendance.objects.filter(Q(user_id=self.kwargs.get('id')) & Q(date__gte=from_date) & Q(date__lte=to_date))
        working_hours = []
        context['ab']=[]
        tmp = []
        for a in abc:
            if a.time_out:

                if a.status is 'absent':
                    wh = 0
                    s = str(wh)
                    working_hours.append(s)

                else:
                    delta = datetime.timedelta(hours=a.time_in.hour, minutes=a.time_in.minute)
                    wh = a.time_out-delta
                    s = str(wh.hour)+" hrs " + str(wh.minute) + " min's"
                    working_hours.append(s)

            else:
                wh = 0
                s = str(wh)
                working_hours.append(s)

            a.working_hours = s
            tmp.append(a)

        context['o'] = tmp

        return context


class CalendarView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('attendance.view_attendance',)
    template_name = 'attendance/calendar.html'
    model = Attendance
    context_object_name = 'attendance'


def download_excel_data(request):
    current_date = datetime.datetime.strptime(request.GET['current_date'], "%Y-%m-%d")
    if request.GET.get('date'):
        from_date = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d")
        to_date = datetime.datetime.strptime(request.GET.get('to_date'), "%Y-%m-%d")
        if Attendance.objects.filter(Q(date__gte=from_date) & Q(date__lte=to_date)):
            attendance = Attendance.objects.filter(Q(date__gte=from_date) & Q(date__lte=to_date))
    elif Attendance.objects.filter(date=current_date):
        attendance = Attendance.objects.filter(date=current_date)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Employee Id', 'Department', 'Name', 'Clock-in', 'Clock-out', 'Late', 'Attendance'])
    for a in attendance:
        writer.writerow([a.date, a.user_id, a.user.department, a.user.first_name, a.time_in, a.time_out, a.note, a.status])

    return response


def download_emp_excel_data(request):
    emp_id = int(request.GET['id'])
    current_date = datetime.datetime.strptime(request.GET['current_date'], "%Y-%m-%d")
    if request.GET.get('date'):
        from_date = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d")
        to_date = datetime.datetime.strptime(request.GET.get('to_date'), "%Y-%m-%d")
        if Attendance.objects.filter(Q(date__gte=from_date) & Q(date__lte=to_date) & Q(user_id=emp_id)):
            attendance = Attendance.objects.filter(Q(date__gte=from_date) & Q(date__lte=to_date) & Q(user_id=emp_id))
    elif Attendance.objects.filter(date=current_date):
        attendance = Attendance.objects.filter(user_id=emp_id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', attendance[0].user.first_name])
    writer.writerow(['Department', attendance[0].user.department])
    writer.writerow(['Date', 'Clock In', 'Clock Out', 'Working Hours', 'Attendance'])
    working_hours = []
    tmp = []
    for a in attendance:
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
            wh = a.time_out - delta
            s = str(wh.hour) + " hrs " + str(wh.minute) + " min's"
            working_hours.append(s)
        a.working_hours = s
        tmp.append(a)
    for a in tmp:
        writer.writerow(
            [a.date, a.time_in, a.time_out, a.working_hours, a.status])

    return response


def attendance_graph(request):
    form = GraphForm(request.GET)

    return render(request, 'attendance/attendancebar.html',{'form':form})


def ajax_data(request):
    data = Attendance.objects.filter(date__year=datetime.datetime.now().year)

    list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    i = 0
    count = 0
    for d in data:
        if d.status == "absent" and d.date.month == i:
            count = count+1
        elif d.status == "absent" and d.date.month != i:
            i = d.date.month
            count = 1
        list1[i - 1] = count

    return JsonResponse(data={'list': list1})


def ajax_data_change(request):
    if request.method == 'GET':
        year = request.GET['year2']
        data = Attendance.objects.filter(date__year=year)
        list2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        i = 0
        count = 0
        for d in data:
            if d.status == "absent" and d.date.month == i:
                count = count + 1
            elif d.status == "absent" and d.date.month != i:
                i = d.date.month
                count = 1
            list2[i - 1] = count
        return JsonResponse(data={'list': list2})






