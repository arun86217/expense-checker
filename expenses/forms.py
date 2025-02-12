from django import forms
from .models import Expense, Income, ExpenseException, IncomeException
from django.core.exceptions import ValidationError
from datetime import date

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

class ExpenseEditForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'tag']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'})
        }

class IncomeEditForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['title', 'amount', 'tag']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'})
        }

class ExpenseExceptionForm(forms.ModelForm):
    class Meta:
        model = ExpenseException
        fields = ['amount', 'date', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date(self):
        exception_date = self.cleaned_data['date']
        if exception_date < date.today():
            raise ValidationError("Cannot create exceptions for past dates")
        return exception_date

class IncomeExceptionForm(forms.ModelForm):
    class Meta:
        model = IncomeException
        fields = ['amount', 'date', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date(self):
        exception_date = self.cleaned_data['date']
        if exception_date < date.today():
            raise ValidationError("Cannot create exceptions for past dates")
        return exception_date 