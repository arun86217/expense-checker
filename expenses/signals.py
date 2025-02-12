from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Expense, Income, ExpenseHistory, IncomeHistory
from django.utils import timezone

@receiver(pre_save, sender=Expense)
def track_expense_changes(sender, instance, **kwargs):
    if instance.pk:  # Only for existing instances
        try:
            old_instance = Expense.objects.get(pk=instance.pk)
            if old_instance.amount != instance.amount:
                ExpenseHistory.objects.create(
                    expense=instance,
                    amount=old_instance.amount,
                    effective_date=old_instance.last_modified.date()
                )
        except Expense.DoesNotExist:
            pass

@receiver(pre_save, sender=Income)
def track_income_changes(sender, instance, **kwargs):
    if instance.pk:  # Only for existing instances
        try:
            old_instance = Income.objects.get(pk=instance.pk)
            if old_instance.amount != instance.amount:
                IncomeHistory.objects.create(
                    income=instance,
                    amount=old_instance.amount,
                    effective_date=old_instance.last_modified.date()
                )
        except Income.DoesNotExist:
            pass 