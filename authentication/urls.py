from .views import RegistrationView, LoginView, UsernameValidationView, EmailValidationView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='username-validate'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='email-validate'),
]
