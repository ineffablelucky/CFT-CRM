from django.urls import path
from .views import Download_salary,CTC
app_name = 'ctc'

urlpatterns = [
    path('',Download_salary.as_view(),name="download_salary"),
    path('ctc/', CTC.as_view(), name="ctc"),
   #path("<int:id1>/<int:id2>/",views.download,name="download"),
]
