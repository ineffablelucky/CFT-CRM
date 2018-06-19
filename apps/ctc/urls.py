from django.shortcuts import render, redirect
from django.urls import path
from . import views
app_name = 'ctc'

urlpatterns = [
    path('',views.index,name="index"),
    path('slip/<int:id/>', views.slip, name="slip"),

]