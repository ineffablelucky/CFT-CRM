from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import TaskList, Employee_Task_List, TaskCreate
app_name = 'task'

urlpatterns = [
    path('', TaskList.as_view(template_name="manager_task_page.html"), name="manager_task_list"),
    path('add/', TaskCreate.as_view(template_name="add_task.html"), name='add_task'),
    path('employee/', Employee_Task_List.as_view(template_name="employee_task_page"), name="employee_task_page"),
]