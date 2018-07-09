from django.contrib import admin
from django.urls import path, include
from apps.opportunity import views
from ..meeting.views import L_Meeting

app_name = 'opportunity'
urlpatterns = [
    path('', views.ListOppo.as_view(), name='list_oppo'),
    path('<int:pk>/change_status/', views.C_Status.as_view(), name='change_status'),
    #path('<int:pk>/change_status/', views.change_status, name='change_status'),
    path('assigned_leads/', views.A_Leads.as_view(), name='assign_lead'),
    path('add_proj_manager/<int:pk>', views.A_PManager.as_view(), name='add_proj_manager'),
    path('closed_leads', views.C_Leads.as_view(), name='closed_leads'),
    path('declined_leads', views.D_Leads.as_view(), name='declined_leads'),
    path('<int:pk>/meeting/', include('apps.meeting.urls', namespace='meeting')),
    path('add_client/', views.CreateClientView.as_view(), name='create_client'),
    path(
        'add_opportunity_existing_client/',
        views.UpdateClientOpportunityView.as_view(),
        name='add_opportunity_existing_client'),
    path('client_list/', views.ListClient.as_view(), name='client_list'),
    path('client_list/<int:pk>/', views.ListClientOpportunity.as_view(), name='client_list_opportunity')
]