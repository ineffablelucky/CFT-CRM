from django.urls import path
from . import views
from django.views.generic import TemplateView
app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.auth_login, name='login'),
    path('register/', views.register, name='register'),
    path('login/profile/<int:id>', views.profile, name='profile'),
    path('login/welcome/', views.welcome, name='welcome'),
    path('logout/', views.lout, name='logout'),

    path('about/', TemplateView.as_view(template_name="production/index.html")),
]

