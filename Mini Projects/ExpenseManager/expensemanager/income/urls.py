from django.urls import path
from. import views

urlpatterns = [
    path('',views.index,name="income"),
    path('add-income',views.add_income,name="add-income"),
    path('edit-expense/<int:id>', views.income_edit, name="income-edit"),
    path('income-delete/<int:id>',views.delete_income,name='income-delete'),
]