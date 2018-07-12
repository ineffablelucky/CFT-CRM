from django.urls import path,include
from django.views.generic import TemplateView,ListView
from .import views



from configs import settings
app_name='leads'
urlpatterns =[
    #path('i',views.LeadIndex.as_view(),name='LeadIndex'),
    path('details/',views.LeadDetails.as_view(),name='LeadDetails'),
    path('create/',views.LeadCreate.as_view(),name='LeadCreate'),
    path('edit/<pk>',views.LeadEdit.as_view(),name='LeadEdit'),
    path('delete/<pk>',views.LeadDelete.as_view(),name='LeadDelete'),
    path('details/assign/',views.LeadsAssign,name='leadsassign'),
    path('editajax/<int:id>',views.check),

    path('upload/csv/', views.upload_csv, name='upload_csv'),

    path('downloadpdf/',views.DownloadPdf,name='LeadDownloadpdf'),
    path('downloadcsv/',views.DownloadCsv,name='LeadDownloadcsv'),
    path('api/hello/',views.hello),
    path('api',views.MyUserViewSet)



]
