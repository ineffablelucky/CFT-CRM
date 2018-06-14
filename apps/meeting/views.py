from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.meeting.forms import CreateMeeting
from django.urls import reverse, reverse_lazy
from apps.meeting.models import MEETING


class CMeeting(CreateView):
    form_class = CreateMeeting
    model = MEETING
    template_name = 'meeting/create_meeting.html'
    success_url = '/'
