from django.urls import path
from .views import LeaveCreation, LeaveRequest
app_name = 'leave'

urlpatterns = [
    path('', LeaveCreation.as_view(), name="leave_creation"),
    path('leaverequest', LeaveRequest.as_view(), name="leave_request")
]
