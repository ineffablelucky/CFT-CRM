from django.contrib import admin
from django.urls import path, include
from apps.opportunity import views

app_name = 'opportunity'
urlpatterns = [
    path('', views.ListOppo.as_view(), name='list_oppo'),
    path('change_status/<int:pk>', views.C_Status.as_view(), name='change_status'),
    path('assigned_leads/', views.A_Leads.as_view(), name='assign_lead'),
    path('add_proj_manager/<int:pk>', views.A_PManager.as_view(), name='add_proj_manager'),
    path('closed_leads', views.C_Leads.as_view(), name='closed_leads'),
    path('declined_leads', views.D_Leads.as_view(), name='declined_leads')
]