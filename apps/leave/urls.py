from django.urls import path
from .views import LeaveCreation, LeaveApproval, ShowRequest, Approve, Reject
app_name = 'leave'

urlpatterns = [
    path('', LeaveCreation.as_view(), name="leave_creation"),
    path('leaverequest', LeaveApproval.as_view(), name="leave_request"),
    path('showrequest/<int:id>', ShowRequest.as_view(), name="show_request"),
    path('showrequest/approve/<int:id>', Approve.as_view(), name="approve"),
    path('showrequest/reject/<int:id>', Reject.as_view(), name="reject"),
    #path('employeeattendance', EmployeeAttendanceView.as_view(), name="employee_attendance")
]
