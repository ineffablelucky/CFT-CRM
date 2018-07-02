from django.urls import path
from . import views
app_name = "salary_percentages"

urlpatterns = [
    path('', views.salary, name="salary"),
    path('edit_salary/<int:id>/', views.edit_salary, name="edit_salary"),
    path('edit_salary/<int:id>/edit_ctc/',views.edit_ctc,name="edit_ctc"),
    path('edit_salary/<int:id>/edit_bonus/',views.edit_bonus,name="edit_bonus"),
    path('structure/', views.salary_structure, name="salary_structure"),
    path('add/',views.add, name="add"),
    path('upload_csv/',views.upload_csv,name="upload_csv"),

]