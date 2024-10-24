""" urls from personal """
from django.urls import path
from . import views

app_name = "personal"

urlpatterns = [
    path('perfil/atualizar/', views.profile_update, name="profile-update"),
    path('formacao/academica/nova/', views.add_academic_formation, name="add-academic-formation"),
    path('formacao/academica/eliminar/<uuid:id>', views.delete_academic_formation, name="delete-academic-formation"),
    path('formacao/profissional/nova/', views.add_profissional_formation, name="add-profissional-formation"),
    path('formacao/profissional/eliminar/<uuid:id>', views.delete_profissional_formation,
         name="delete-profissional-formation"),

    path('experiencia-profissional/nova/', views.add_profissional_experience, name="add-profissional-experience"),
    path('documentacao/atualizar/', views.add_documentation, name="add-documentation"),

    path('minha-carreira-profissional/', views.career, name="career"),

    path('vagas/', views.vacancy_list, name="vacancy-list"),
    path('vagas/<slug:company_slug>/detalhes/<uuid:vid>/', views.vacancy_detail, name="vacancy-detail"),
    path('candidaturas/adicionar-candidatura/<uuid:vid>/', views.apply_for_vacancy, name="apply-for-vacancy"),

    path('minhas-candidaturas/', views.my_candidates, name="my-candidates"),

    path('perfil-do-usuario/<uuid:uid>', views.user_profile, name="user-profile"),
]