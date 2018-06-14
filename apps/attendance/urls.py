from django.urls import path
from . import views
from .views import LeaveRequest, Completed

app_name = 'attendance'
urlpatterns = [
    path('leave/', LeaveRequest.as_view(), name='leave_request'),
    path('completed/', Completed.as_view(), name='task_completed'),

]