from django.urls import path,include
from . import views
from .views import ListModule, Details_Project

urlpatterns = [
    path('<int:pk>/', Details_Project.as_view(), name="project-details"),
    path('<int:pk>/', ListModule.as_view(), name="module_list"),
]
