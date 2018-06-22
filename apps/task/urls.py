from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import TaskList, Employee_Task_List, TaskCreate, Edit_Task, Details_Task
app_name = 'task'

urlpatterns = [
    path('<int:pk>/', TaskList.as_view(template_name="task_manager_list.html"), name="manager-task-view"),

    # path('<int:pk>/add/', TaskCreate.as_view(), name='task-add'),
    path('add/', TaskCreate.as_view(), name='task-add'),
    path('update/<int:pk>/', Edit_Task.as_view(), name='task-update'),
    path('details/<int:pk>/', Details_Task.as_view(), name="task-details"),

    path('employee/', Employee_Task_List.as_view(template_name="my tasks.html"), name="employee-task-list"),

]