from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import TaskList, Employee_Task_List, TaskCreate, Edit_Task, Details_Task
app_name = 'task'

urlpatterns = [
    path('<int:pk>/', TaskList.as_view(), name="manager-task-view"),

    # path('<int:pk>/add/', TaskCreate.as_view(), name='task-add'),
    path('add/', TaskCreate.as_view(), name='task-add'),
    path('update/<int:pk>/', Edit_Task.as_view(), name='task-update'),

    # path('details/<int:pk>/start/', Start_Task.as_view(), name='taskstart'),
    # path('details/<int:pk>/end/', End_Task.as_view(), name='taskend'),
    path('details/<int:pk>/start', views.entry, name='taskstart'),
    path('details/<int:pk>/end/', views.end, name='taskend'),
    path('details/<int:pk>/', Details_Task.as_view(), name="task-details"),

    path('employee/', Employee_Task_List.as_view(template_name="my tasks.html"), name="employee-task-list"),

]