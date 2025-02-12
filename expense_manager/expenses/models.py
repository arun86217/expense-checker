from django.db import models
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import calendar

class RecurrenceType(models.TextChoices):
    MONTHLY = 'monthly', 'Monthly'
    QUARTERLY = 'quarterly', 'Quarterly'
    HALF_YEARLY = 'half_yearly', 'Half Yearly'
    YEARLY = 'yearly', 'Yearly'
    CUSTOM = 'custom', 'Custom Days'

class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    recurrence_type = models.CharField(
        max_length=20,
        choices=RecurrenceType.choices,
        default=RecurrenceType.MONTHLY
    )
    custom_days = models.IntegerField(null=True, blank=True, 
        help_text="Days between occurrences for custom recurrence")
    occurrences = models.IntegerField(null=True, blank=True,
        help_text="Number of occurrences if end_date not specified")
    tag = models.CharField(max_length=50, blank=True)
    
    def clean(self):
        if not self.end_date and not self.occurrences:
            raise ValidationError("Either end date or number of occurrences must be specified")
        if self.recurrence_type == RecurrenceType.CUSTOM and not self.custom_days:
            raise ValidationError("Custom days must be specified for custom recurrence type")
    
    def get_occurrences(self):
        occurrences = []
        current_date = self.start_date
        
        if self.end_date:
            end_date = self.end_date
        elif self.occurrences:
            if self.recurrence_type == RecurrenceType.MONTHLY:
                end_date = self.start_date + relativedelta(months=self.occurrences)
            elif self.recurrence_type == RecurrenceType.QUARTERLY:
                end_date = self.start_date + relativedelta(months=self.occurrences * 3)
            elif self.recurrence_type == RecurrenceType.HALF_YEARLY:
                end_date = self.start_date + relativedelta(months=self.occurrences * 6)
            elif self.recurrence_type == RecurrenceType.YEARLY:
                end_date = self.start_date + relativedelta(years=self.occurrences)
            else:  # custom
                end_date = self.start_date + relativedelta(days=self.occurrences * self.custom_days)
        
        while current_date <= end_date:
            occurrences.append({
                'date': current_date,
                'amount': self.amount,
                'title': self.title,
                'tag': self.tag
            })
            
            if self.recurrence_type == RecurrenceType.MONTHLY:
                current_date += relativedelta(months=1)
            elif self.recurrence_type == RecurrenceType.QUARTERLY:
                current_date += relativedelta(months=3)
            elif self.recurrence_type == RecurrenceType.HALF_YEARLY:
                current_date += relativedelta(months=6)
            elif self.recurrence_type == RecurrenceType.YEARLY:
                current_date += relativedelta(years=1)
            else:  # custom
                current_date += relativedelta(days=self.custom_days)
        
        return occurrences

class Income(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    is_recurring = models.BooleanField(default=False)
    recurrence_type = models.CharField(
        max_length=20,
        choices=RecurrenceType.choices,
        default=RecurrenceType.MONTHLY,
        blank=True,
        null=True
    )
    tag = models.CharField(max_length=50, blank=True) 