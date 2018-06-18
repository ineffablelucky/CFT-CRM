from django.urls import path

from .views import LeaveRequest, Completed, Clockin, Clock, Clockout

app_name = 'attendance'
urlpatterns = [
    path('leave/', LeaveRequest.as_view(), name='leave_request'),
    path('completed/', Completed.as_view(), name='task_completed'),
    path('clock/', Clock.as_view(), name='clock'),
    path('clock/in/', Clockin.as_view(), name='clockin'),
    path('clock/out/', Clockout.as_view(), name='clockout')

]