from django.urls import path
from .views import *

urlpatterns = [
    path("dashboard/categories/create/", create_category, name="create_category"),
    path("dashboard/categories/", list_categories, name="list_categories"),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/incomes', list_incomes, name='list_incomes'),
    path("incomes/create/", create_income, name="create_income"),
    path("dashboard/expenses", list_expenses, name="list_expenses"),
    path("expenses/create/", create_expense, name="create_expense"),

]
