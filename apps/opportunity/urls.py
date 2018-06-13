from django.contrib import admin
from django.urls import path, include
from apps.opportunity import views


urlpatterns = [
    path('', views.ListOppo.as_view(), name='list_oppo'),
    path('change_status/<int:pk>', views.C_Status.as_view(), name='change_status')
]