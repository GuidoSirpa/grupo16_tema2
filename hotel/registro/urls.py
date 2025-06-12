from django.contrib.auth import views as auth_views

from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('accounts/logout/', LogoutView.as_view(next_page='/accounts/login/', http_method_names=['get', 'post']), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registro/login.html'), name='login'),
     
]
