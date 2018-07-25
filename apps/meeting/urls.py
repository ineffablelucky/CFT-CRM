from django.urls import path
from apps.meeting import views


app_name = 'meeting'
urlpatterns = [
    path('create_meeting/', views.CMeeting.as_view(), name='create_meeting'),
    path('meeting_list/', views.L_Meeting.as_view(), name='meeting_list'),
    path('employee_meeting/', views.Emp_Meetings.as_view(), name='emp_meeting'),
    path(
        'employee_meeting/<int:meeting_id>/add_meeting_notes',
        views.AddMeetingNotesView.as_view(),
        name='add_meeting_notes'
    )
]