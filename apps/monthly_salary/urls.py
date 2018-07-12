from django.urls import path
from . import views
app_name = "monthly_salary"

urlpatterns = [

    path('edit_salary/',views.edit_salary_list,name="edit_salary_list"),
    path('edit_salary/<int:id>/',views.edit_salary,name="edit_salary"),
    path('monthly_salary/',views.monthly_salary_list,name="monthly_salary_list"),
    path('monthly_salary/<int:id>/',views.monthly_salary,name="monthly_salary")

]