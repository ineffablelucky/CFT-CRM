from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.meeting.forms import CreateMeeting
from django.urls import reverse, reverse_lazy
from apps.meeting.models import MEETING


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
