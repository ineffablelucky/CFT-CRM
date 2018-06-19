from django.shortcuts import redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateleaveForm
from ..attendance.models import Attendance
from ..users.models import MyUser
from django.db.models import Q

class LeaveCreation(CreateView):
    form_class = CreateleaveForm
    template_name = 'assignleave.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return redirect('/')


class LeaveRequest(LoginRequiredMixin, ListView):
    template_name = 'leaves.html'
    model = Attendance
    context_object_name = 'myuser'

    def get_queryset(self):
        queryset = Attendance.objects.filter(status='Pending')
        return queryset
