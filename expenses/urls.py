from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('expenses/', views.ExpenseListView.as_view(), name='expense-list'),
    path('expenses/add/', views.ExpenseCreateView.as_view(), name='expense-add'),
    path('incomes/', views.IncomeListView.as_view(), name='income-list'),
    path('incomes/add/', views.IncomeCreateView.as_view(), name='income-add'),
    path('month/<int:year>/<int:month>/', views.month_detail, name='month-detail'),
    path('expenses/<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='expense-edit'),
    path('incomes/<int:pk>/edit/', views.IncomeUpdateView.as_view(), name='income-edit'),
    path('expenses/<int:expense_id>/exception/', 
         views.ExpenseExceptionCreateView.as_view(), 
         name='expense-exception'),
    path('incomes/<int:income_id>/exception/', 
         views.IncomeExceptionCreateView.as_view(), 
         name='income-exception'),
] 