from django import forms
from .models import Expense, Income

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'start_date', 'end_date', 
                 'recurrence_type', 'custom_days', 'occurrences', 'tag']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['title', 'amount', 'date', 'is_recurring', 
                 'recurrence_type', 'tag']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        } 