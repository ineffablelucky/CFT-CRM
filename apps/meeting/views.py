from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.meeting.forms import CreateMeeting
from django.urls import reverse, reverse_lazy
from apps.meeting.models import MEETING
from apps.opportunity.models import Opportunity
from django.db.models import Q


class CMeeting(CreateView):
    form_class = CreateMeeting
    model = MEETING
    template_name = 'meeting/create_meeting.html'
    success_url = reverse_lazy('meeting: meeting_list')


class L_Meeting(ListView):
    model = MEETING
    template_name = 'opportunity/meeting_list.html'
    context_object_name = 'meetings'
    print('Listing Meeting List')


class Emp_Meetings(ListView):
    print("heelo Mooto")
    model = MEETING
    template_name = 'meeting/employee_meeting.html'
    context_object_name = 'emp_meeting'

    def get_queryset(self):
        temp= Opportunity.objects.filter(assigned_to=self.request.user)
        queryset1 = MEETING.objects.filter(Opportunity=temp)
        print(queryset1)

        queryset2 = self.request.user.meetings_extra.all()
        print(queryset2)
        return None
