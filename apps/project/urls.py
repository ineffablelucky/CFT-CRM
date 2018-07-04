from django.urls import path, include
from django.views.generic import TemplateView
from . import views

from .views import ProjectList, Employee_Project_List, ProjectCreate, Edit_Project, ListModule, OppProjectList
from apps.task.views import Employee_Task_List
app_name = 'project'

urlpatterns = [

    path('', ProjectList.as_view(), name="project_manager_list"),
    path('opp/', OppProjectList.as_view(), name='opportunity-projects'),

    path('add/', ProjectCreate.as_view(), name='project-add'),
    path('update/<int:pk>/', Edit_Project.as_view(), name='project-update'),
    # path('opp/update/<int:pk>/', Edit_Project_opp.as_view(), name='project-opp-update'),
    path('details/<int:pk>/', ListModule.as_view(), name="project-details"),

    path('employee/', Employee_Project_List.as_view(), name="employee-project"),


    path('', include('apps.task.urls')),
]