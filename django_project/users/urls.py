"""Defines URL patterns for users"""
from django.urls import re_path, reverse
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    # Login page
    re_path(r'^login/$', LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True),
            name='login'),

    # Logout Page
    re_path(r'^logout/$', LogoutView.as_view(next_page='/'), name='logout'),

    # Registration Page
    re_path(r'^register/$', views.register, name='register'),
]