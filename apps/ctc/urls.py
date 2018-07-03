from django.urls import path
from .views import Salary,CTC,Download_Salary
from . import views
app_name = 'ctc'

urlpatterns = [
    path('',Salary.as_view(),name="salary"),
    path('ctc/', CTC.as_view(), name="ctc"),
    path("download_salary/<int:id1>/<int:id2>/",views.Download_Salary,name="download_salary"),
]
