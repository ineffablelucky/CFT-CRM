from django.contrib import admin
from django.urls import path, include
from apps.opportunity.views import ListOppo


urlpatterns = [
    path('', ListOppo.as_view(), name='list_oppo'),
]