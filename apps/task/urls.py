from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.project_manager_task_index, name="task_index"),
    path('employee/', views.employee_task_index, name="employee_task_index"),
]
