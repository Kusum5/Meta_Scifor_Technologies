from django.urls import path
from .views import RegistrationView, UsernameValidationView, EmailValidationView, LoginView, LogoutView

urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('validate-username', UsernameValidationView.as_view(),name="validate-username"),
    path('validate-email', EmailValidationView.as_view(),name="validate-email"),
    path('login',LoginView.as_view(),name="login"),
    path('logout',LogoutView.as_view(),name="logout"),
]