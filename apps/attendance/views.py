from django.shortcuts import render
from .forms import LeaveForm


def leave_request(request):
    form = LeaveForm()
    return render(request, 'leaverequest.html', {'form' : form})

