from django.urls import path
from apps.meeting import views


app_name = 'meeting'
urlpatterns = [
    path('create_meeting/', views.CMeeting.as_view(), name='create_meeting'),
]