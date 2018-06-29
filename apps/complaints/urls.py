from django.urls import path
from .import views


app_name = 'complaints'
urlpatterns =[

    path('createcomplaints/',views.createComplaints.as_view(),name='createComplaints'),
    path('createcomplaints/complaints_ajax/',views.complaints_ajax,name='complaints'),




]