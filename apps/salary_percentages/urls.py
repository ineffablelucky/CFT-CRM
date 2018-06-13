from django.shortcuts import render, redirect
from django.urls import path
from . import views
app_name = 'salary_percentages'

urlpatterns = [
    path('', views.table, name="index"),
    path('add/',views.add, name="add"),

]