from django.urls import path
from .views import  LoginView, RegistrationView , ProfileView

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
]