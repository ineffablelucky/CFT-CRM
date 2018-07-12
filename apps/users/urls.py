from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import EmployeeProfile



app_name = 'users'

urlpatterns = [
    path('', views.auth_login, name='login'),
    path('login/welcome/', views.welcome, name='welcome'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-welcome/', TemplateView.as_view(template_name="apps/users/templates/users/base.html"), name='admin_welcome'),
    path('register/', views.register, name='register'),
    path('profile/', views.my_profile, name='profile'),
    path('edit-profile/', views.edit_self, name='edit_profile'),
    path('login/profile-all/', EmployeeProfile.as_view(), name='profile_all'),
    path('edit-emp/<int:pk>', views.EditEmployeeProfile.as_view(), name='edit_emp'),
    path('logout/', views.lout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('sendemail/', views.sendEmail, name='sendmail'),
    path('token/', views.reset_password, name='token'),
    path('reset-link/<str:key>/', views.verify, name='verify'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('api/register/',views.create_auth),
    path('api/login/',views.login_api)


]
