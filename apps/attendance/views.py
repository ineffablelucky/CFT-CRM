from django.shortcuts import render
from .forms import LeaveForm
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class LeaveRequest(LoginRequiredMixin, CreateView):
    form_class = LeaveForm
    template_name = 'leaverequest.html'

    def get_form_kwargs(self):
        """Returns the keyword arguments for instantiating the form"""
        kwargs = super().get_form_kwargs()
        kwargs.update({'logged_user': self.request.user})
        kwargs = {'logged_user' : self.request.user}
        return kwargs



