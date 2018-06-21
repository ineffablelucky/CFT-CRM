from django.urls import path
from .views import Index,CTC
app_name = 'ctc'

urlpatterns = [
    path('',Index.as_view(),name="index"),
    path('ctc/', CTC.as_view(), name="ctc"),
   # path("<int:id1>/<int:id2>/",views.download,name="download"),
]
