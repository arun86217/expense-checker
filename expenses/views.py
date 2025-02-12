from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Expense, Income, ExpenseException, IncomeException
from .forms import ExpenseForm, IncomeForm, ExpenseEditForm, IncomeEditForm, ExpenseExceptionForm, IncomeExceptionForm
from datetime import datetime
from collections import defaultdict
from django.db.models import Sum
import calendar
from django.contrib import messages
from django.db import IntegrityError
from .utils import format_indian_currency

def dashboard(request):
    try:
        # Get the year from query parameters or use current year
        current_year = int(request.GET.get('year', datetime.now().year))
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
        
        # Get all incomes and their occurrences
        incomes = Income.objects.all()
        income_totals = defaultdict(float)
        
        for income in incomes:
            occurrences = income.get_occurrences()
            for occurrence in occurrences:
                month_key = occurrence['date'].strftime('%Y-%m')
                income_totals[month_key] += float(occurrence['amount'])
        
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
        
        context = {
            'year': current_year,
            'months': [{
                'name': month['name'],
                'number': month['number'],
                'expenses': month['expenses'],
                'total_expenses': format_indian_currency(month['total_expenses']),
                'total_income': format_indian_currency(month['total_income']),
                'balance': format_indian_currency(month['balance'])
            } for month in months],
            'prev_year': current_year - 1,
            'next_year': current_year + 1
        }
        return render(request, 'expenses/dashboard.html', context)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return render(request, 'expenses/dashboard.html', {
            'months': [],
            'year': datetime.now().year
        })

class ExpenseListView(ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        return Expense.objects.all().order_by('start_date')

class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:expense-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_actions'] = True
        return context

class IncomeListView(ListView):
    model = Income
    template_name = 'expenses/income_list.html'
    context_object_name = 'incomes'

    def get_queryset(self):
        return Income.objects.all().order_by('date')

class IncomeCreateView(CreateView):
    model = Income
    form_class = IncomeForm
    template_name = 'expenses/income_form.html'
    success_url = reverse_lazy('expenses:income-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_actions'] = True
        return context

def month_detail(request, year, month):
    month_name = calendar.month_name[month]
    
    # Get expenses for the month
    expenses = Expense.objects.all()
    month_expenses = []
    
    for expense in expenses:
        occurrences = expense.get_occurrences()
        for occurrence in occurrences:
            if occurrence['date'].year == year and occurrence['date'].month == month:
                # Add the expense ID and original date to the occurrence
                occurrence['id'] = expense.id
                occurrence['original_date'] = occurrence['date']
                month_expenses.append(occurrence)
    
    # Get incomes for the month
    incomes = Income.objects.all()
    month_incomes = []
    
    for income in incomes:
        occurrences = income.get_occurrences()
        for occurrence in occurrences:
            if occurrence['date'].year == year and occurrence['date'].month == month:
                # Add the income ID and original date to the occurrence
                occurrence['id'] = income.id
                occurrence['original_date'] = occurrence['date']
                month_incomes.append(occurrence)
    
    total_expenses = sum(float(expense['amount']) for expense in month_expenses)
    total_income = sum(float(income['amount']) for income in month_incomes)
    
    return render(request, 'expenses/month_detail.html', {
        'year': year,
        'month': month,
        'month_name': month_name,
        'expenses': month_expenses,
        'incomes': month_incomes,
        'total_expenses': total_expenses,
        'total_income': total_income,
        'balance': total_income - total_expenses
    })

class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseEditForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:expense-list')

    def form_valid(self, form):
        messages.success(self.request, 'Expense updated. Past occurrences will maintain their historical values.')
        return super().form_valid(form)

class IncomeUpdateView(UpdateView):
    model = Income
    form_class = IncomeEditForm
    template_name = 'expenses/income_form.html'
    success_url = reverse_lazy('expenses:income-list')

    def form_valid(self, form):
        messages.success(self.request, 'Income updated. Past occurrences will maintain their historical values.')
        return super().form_valid(form)

class ExpenseExceptionCreateView(CreateView):
    model = ExpenseException
    form_class = ExpenseExceptionForm
    template_name = 'expenses/exception_form.html'
    
    def get_success_url(self):
        return reverse_lazy('expenses:month-detail', kwargs={
            'year': self.object.date.year,
            'month': self.object.date.month
        })
    
    def form_valid(self, form):
        form.instance.expense_id = self.kwargs.get('expense_id')
        date = form.cleaned_data['date']
        
        try:
            # Try to find an existing exception for this expense
            existing_exception = ExpenseException.objects.filter(
                expense_id=form.instance.expense_id,
                original_date=self.request.GET.get('date')
            ).first()
            
            if existing_exception:
                # Update existing exception
                existing_exception.date = date
                existing_exception.amount = form.cleaned_data['amount']
                existing_exception.reason = form.cleaned_data['reason']
                existing_exception.save()
                self.object = existing_exception
                messages.info(self.request, 
                    f"Updated exception for {existing_exception.expense.title} to {date}")
                return redirect(self.get_success_url())
            else:
                # Create new exception
                response = super().form_valid(form)
                messages.success(self.request, 
                    f"Exception added for {self.object.expense.title} on {date}")
                return response
                
        except IntegrityError:
            messages.error(self.request, 
                f"An exception already exists for this date. Please choose a different date.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expense = get_object_or_404(Expense, pk=self.kwargs['expense_id'])
        context['expense'] = expense
        
        # Get the original date from query params
        original_date = self.request.GET.get('date')
        if original_date:
            # Find exception by original date
            existing_exception = ExpenseException.objects.filter(
                expense_id=self.kwargs['expense_id'],
                original_date=original_date
            ).first()
            
            if existing_exception:
                context['existing_exception'] = existing_exception
                if not context.get('form').is_bound:
                    context['form'].initial = {
                        'amount': existing_exception.amount,
                        'date': existing_exception.date,
                        'reason': existing_exception.reason
                    }
            else:
                # Pre-populate the date field for new exceptions
                context['form'].initial = {'date': original_date}
        
        return context

class IncomeExceptionCreateView(CreateView):
    model = IncomeException
    form_class = IncomeExceptionForm
    template_name = 'expenses/exception_form.html'
    
    def get_success_url(self):
        return reverse_lazy('expenses:month-detail', kwargs={
            'year': self.object.date.year,
            'month': self.object.date.month
        })
    
    def form_valid(self, form):
        form.instance.income_id = self.kwargs.get('income_id')
        date = form.cleaned_data['date']
        
        try:
            # Try to find an existing exception for this income
            existing_exception = IncomeException.objects.filter(
                income_id=form.instance.income_id,
                original_date=self.request.GET.get('date')
            ).first()
            
            if existing_exception:
                # Update existing exception
                existing_exception.date = date
                existing_exception.amount = form.cleaned_data['amount']
                existing_exception.reason = form.cleaned_data['reason']
                existing_exception.save()
                self.object = existing_exception
                messages.info(self.request, 
                    f"Updated exception for {existing_exception.income.title} to {date}")
                return redirect(self.get_success_url())
            else:
                # Create new exception
                response = super().form_valid(form)
                messages.success(self.request, 
                    f"Exception added for {self.object.income.title} on {date}")
                return response
                
        except IntegrityError:
            messages.error(self.request, 
                f"An exception already exists for this date. Please choose a different date.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        income = get_object_or_404(Income, pk=self.kwargs['income_id'])
        context['income'] = income
        
        # Get the original date from query params
        original_date = self.request.GET.get('date')
        if original_date:
            # Find exception by original date
            existing_exception = IncomeException.objects.filter(
                income_id=self.kwargs['income_id'],
                original_date=original_date
            ).first()
            
            if existing_exception:
                context['existing_exception'] = existing_exception
                if not context.get('form').is_bound:
                    context['form'].initial = {
                        'amount': existing_exception.amount,
                        'date': existing_exception.date,
                        'reason': existing_exception.reason
                    }
            else:
                # Pre-populate the date field for new exceptions
                context['form'].initial = {'date': original_date}
        
        return context 