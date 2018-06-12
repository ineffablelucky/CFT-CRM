from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.module_index, name="task_index"),
]
