from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from apps.meeting.forms import CreateMeeting
from django.urls import reverse, reverse_lazy
from apps.meeting.models import MEETING
from apps.opportunity.models import Opportunity
from django.db.models import Q


class CMeeting(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    print('Hello World')
    permission_required = (
         'users.view_meeting',
         'meeting.add_meeting',
         'meeting.change_meeting',
         'meeting.delete_meeting',
    )
    form_class = CreateMeeting
    model = MEETING
    template_name = 'meeting/create_meeting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['oppo_id'] = self.kwargs.get('pk')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'oppo_id': self.kwargs.get('pk')})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('opportunity:meeting:meeting_list', kwargs=self.kwargs)


class L_Meeting(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = (
        'users.view_meeting',
        # 'meeting.change_meeting',
    )
    model = MEETING
    template_name = 'meeting/meeting_list.html'
    context_object_name = 'meetings'

    def get_queryset(self):
        queryset = MEETING.objects.filter(Opportunity__id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['oppo_id'] = self.kwargs.get('pk')
        return context


class Emp_Meetings(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = (
        'users.view_meeting',
        'meeting.change_meeting',
    )
    print("heelo Mooto")
    model = MEETING
    template_name = 'meeting/employee_meeting.html'
    context_object_name = 'emp_meeting'

    def get_queryset(self):
        queryset = MEETING.objects.filter(Q(Opportunity__id=self.kwargs.get('pk')))
        return queryset
    # def get_queryset(self):
    #     print('@@@@@@@@@@@@@@@@@@@@@@@@@')
    #     print(self.kwargs)
    #     temp = MEETING.objects.filter(Opportunity__assigned_to=self.request.user)
    #     print('printing temp')
    #     print(temp)
    #     queryset1 = MEETING.objects.filter(Opportunity=temp)
    #     #print(queryset1)
    #
    #     queryset2 = self.request.user.meetings_extra.all()
    #     #print(queryset2)
    #     return None
