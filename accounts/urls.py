from django.urls import path
from .views import (
    RegistrationView,LoginView,LogoutView,ProfileView
    )

urlpatterns = [
    path('signup/',RegistrationView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('log-out/',LogoutView.as_view(),name='logout'),
    path('profile/',ProfileView.as_view(),name='profile')
]