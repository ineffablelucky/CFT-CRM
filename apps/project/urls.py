from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    #path('', TemplateView.as_view(template_name="project_manager_view.html")),
    path('', views.project_manager_index, name="project_manager_index"),
    path('employee/', views.employee_project, name="employee_project"),
    path('create/', views.create_project_form, name="CreateProjectForm"),
]