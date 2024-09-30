from django.urls import path
from . import views

urlpatterns = [
    path('',views.user_list,name="user_list"),
    path('user/<int:pk>/',views.user_detail,name="user_detail"),
    path('user/new',views.user_list,name="user_create"),
    path('user/<int:pk>/edit/',views.user_list,name="user_update"),
    path('user/<int:pk>/delete/',views.user_list,name="user_delete"),
]