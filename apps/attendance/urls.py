from django.urls import path
from . import views
from .views import LeaveRequest

urlpatterns = [
    path('leave/', LeaveRequest.as_view(), name='leave_request'),
]