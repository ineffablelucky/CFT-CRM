from django.urls import path
from . import views
app_name = "salary_percentages"

urlpatterns = [
    path('', views.salary_structure, name="salary_structure"),
    path('add/',views.add, name="add"),
    path('upload_csv/',views.upload_csv,name="upload_csv"),

]