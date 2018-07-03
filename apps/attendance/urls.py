from django.urls import path
from .views import LeaveRequestView, Completed, Clockin, Clock, Clockout, PastAttendance, ShowAttendance, EmployAttendance
from .views import CalendarView
from . import views

app_name = 'attendance'
urlpatterns = [
    path('leave/', LeaveRequestView.as_view(), name='leave_request'),
    path('completed/', Completed.as_view(), name='task_completed'),
    #path('clock/', Clock.as_view(), name='clock'),
    path('clock/in/', Clockin.as_view(), name='clockin'),
    path('clock/out/', Clockout.as_view(), name='clockout'),
    path('userattendance/', PastAttendance.as_view(), name='pastattendance'),
    path('', ShowAttendance.as_view(), name='show_attendance'),
    path('showattendance/<int:id>', EmployAttendance.as_view(), name='employ_attendance'),
    path('calendar', CalendarView.as_view(), name='calendar'),
    path('download/', views.download_excel_data, name='download'),
    path('emp_attendance_download/', views.download_emp_excel_data, name='emp_download')

]


