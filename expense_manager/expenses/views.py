from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Expense, Income
from .forms import ExpenseForm, IncomeForm
from datetime import datetime
from collections import defaultdict
from django.db.models import Sum
import calendar

def dashboard(request):
    current_year = datetime.now().year
    months = []
    
    # Get all expenses and their occurrences
    expenses = Expense.objects.all()
    expense_occurrences = defaultdict(list)
    monthly_totals = defaultdict(float)
    
    for expense in expenses:
        occurrences = expense.get_occurrences()
        for occurrence in occurrences:
            month_key = occurrence['date'].strftime('%Y-%m')
            expense_occurrences[month_key].append(occurrence)
            monthly_totals[month_key] += float(occurrence['amount'])
    
    # Get all incomes
    incomes = Income.objects.all()
    income_totals = defaultdict(float)
    
    for income in incomes:
        month_key = income.date.strftime('%Y-%m')
        income_totals[month_key] += float(income.amount)
    
    # Prepare calendar data
    for month in range(1, 13):
        month_key = f'{current_year}-{month:02d}'
        months.append({
            'name': calendar.month_name[month],
            'number': month,
            'expenses': expense_occurrences[month_key],
            'total_expenses': monthly_totals[month_key],
            'total_income': income_totals[month_key],
            'balance': income_totals[month_key] - monthly_totals[month_key]
        })
    
    return render(request, 'expenses/dashboard.html', {
        'months': months,
        'year': current_year
    })

class ExpenseListView(ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'

class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense-list')

class IncomeListView(ListView):
    model = Income
    template_name = 'expenses/income_list.html'
    context_object_name = 'incomes'

class IncomeCreateView(CreateView):
    model = Income
    form_class = IncomeForm
    template_name = 'expenses/income_form.html'
    success_url = reverse_lazy('income-list')

def month_detail(request, year, month):
    month_name = calendar.month_name[month]
    
    # Get expenses for the month
    expenses = Expense.objects.all()
    month_expenses = []
    
    for expense in expenses:
        occurrences = expense.get_occurrences()
        for occurrence in occurrences:
            if occurrence['date'].year == year and occurrence['date'].month == month:
                month_expenses.append(occurrence)
    
    # Get incomes for the month
    incomes = Income.objects.filter(
        date__year=year,
        date__month=month
    )
    
    total_expenses = sum(float(expense['amount']) for expense in month_expenses)
    total_income = sum(float(income.amount) for income in incomes)
    
    return render(request, 'expenses/month_detail.html', {
        'year': year,
        'month': month,
        'month_name': month_name,
        'expenses': month_expenses,
        'incomes': incomes,
        'total_expenses': total_expenses,
        'total_income': total_income,
        'balance': total_income - total_expenses
    }) 