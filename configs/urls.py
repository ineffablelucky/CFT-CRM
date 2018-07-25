"""configs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('attendance/', include('apps.attendance.urls')),
    path('', include('apps.users.urls')),
    path('project/', include('apps.project.urls')),
    path('task/', include('apps.task.urls')),
    path('module/', include('apps.module.urls')),
    path('opportunity/', include('apps.opportunity.urls')),
    path('salary_structure/', include('apps.salary_percentages.urls')),
    path('leads/', include('apps.leads.urls')),
    path('leave/', include('apps.leave.urls')),
    path('salary/', include('apps.ctc.urls')),
    path('complaints/',include('apps.complaints.urls')),
    path('',include('apps.monthly_salary.urls')),
]
