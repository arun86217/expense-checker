from django.contrib import admin
from django.urls import path
from expenses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('expenses/', views.ExpenseListView.as_view(), name='expense-list'),
    path('expenses/add/', views.ExpenseCreateView.as_view(), name='expense-add'),
    path('incomes/', views.IncomeListView.as_view(), name='income-list'),
    path('incomes/add/', views.IncomeCreateView.as_view(), name='income-add'),
    path('month/<int:year>/<int:month>/', views.month_detail, name='month-detail'),
] 