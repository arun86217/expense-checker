from django.contrib import admin
from .models import Expense, Income

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'start_date', 'end_date', 'recurrence_type', 'tag')
    list_filter = ('recurrence_type', 'tag')
    search_fields = ('title', 'tag')
    date_hierarchy = 'start_date'

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'date', 'is_recurring', 'recurrence_type', 'tag')
    list_filter = ('is_recurring', 'recurrence_type', 'tag')
    search_fields = ('title', 'tag')
    date_hierarchy = 'date' 