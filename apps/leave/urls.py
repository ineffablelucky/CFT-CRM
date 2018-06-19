from django.urls import path
from .views import LeaveCreation
app_name = 'leave'

urlpatterns = [
    path('', LeaveCreation.as_view(), name="leave_creation"),
]
