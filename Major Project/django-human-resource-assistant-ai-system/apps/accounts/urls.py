from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("registo-particular/", views.signup_personal, name="signup-personal"),
    path("registo-empresarial/", views.signup_business, name="signup-business"),
    path("recuperacao-de-palavra-passe/", views.password_reset, name="password-reset"),
    path("alterar-palavra-passe/", views.password_change, name="password-change"),
    path("controller/", views.account_controller, name="controller"),
    # path('ver-perfil/', views.password_change, name="profile"),
    # path('editar-perfil/', views.password_change, name="password-change"),
]