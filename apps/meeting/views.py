from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from apps.meeting.forms import CreateMeeting, AddMeetingNotes
from django.urls import reverse, reverse_lazy
from apps.meeting.models import MEETING
from apps.opportunity.models import Opportunity
from django.db.models import Q


class CMeeting(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = (
         'users.view_users',
         'meeting.view_meeting',
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
        'users.view_users',
        'meeting.view_meeting',
        'meeting.change_meeting',
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

"""
Add PermissionRequiredMixin after editing
"""


class Emp_Meetings(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = (
        'meeting.view_meeting',
        'meeting.change_meeting',
        'opportunity.change_opportunity'
    )

    model = MEETING
    template_name = 'meeting/employee_meeting.html'
    context_object_name = 'emp_meeting'

    def get_queryset(self):
        # print('printing emp meetings')
        # print(self.request.user)
        queryset = MEETING.objects.filter(Q(Opportunity__id=self.kwargs.get('pk')))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        form = AddMeetingNotes(initial={'logged_user': self.request.user})
        context['form'] = form
        #print(form)
        return context

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'editing_user': self.request.user})
    #     print(kwargs)
    #     return kwargs


class AddMeetingNotesView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    form_class = AddMeetingNotes
    model = MEETING
    permission_required = ('meeting.view_meeting', 'meeting.change_meeting',)

    def get_success_url(self):
        return reverse_lazy('opportunity:meeting:emp_meeting', args=[self.kwargs['pk']])

    def get_object(self):
        return MEETING.objects.get(pk=self.kwargs.get('meeting_id'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update()
        # print('Printing get_form_kwargs')
        # print('printing kwargs $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        kwargs['initial'].update({'logged_user': self.request.user})
        #print(kwargs['initial'])
        return kwargs
