from django.db import models
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import calendar
from datetime import date

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
        help_text="Day of month for custom recurrence (1-31)")
    custom_months_interval = models.IntegerField(null=True, blank=True,
        help_text="Number of months between occurrences")
    occurrences = models.IntegerField(null=True, blank=True,
        help_text="Number of occurrences if end_date not specified")
    tag = models.CharField(max_length=50, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def clean(self):
        if not self.end_date and not self.occurrences:
            raise ValidationError("Either end date or number of occurrences must be specified")
        if self.recurrence_type == RecurrenceType.CUSTOM:
            if not self.custom_days or not (1 <= self.custom_days <= 31):
                raise ValidationError("Custom days must be between 1 and 31")
            if not self.custom_months_interval:
                self.custom_months_interval = 1  # Set default interval
    
    def get_occurrences(self, reference_date=None):
        occurrences = []
        current_date = self.start_date
        reference_date = reference_date or date.today()
        
        # Get all exceptions for this expense
        exceptions = {ex.date: ex.amount for ex in self.exceptions.all()}
        
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
            elif self.recurrence_type == RecurrenceType.CUSTOM and self.custom_months_interval:
                # Only calculate if custom_months_interval is set
                end_date = self.start_date + relativedelta(months=self.occurrences * (self.custom_months_interval or 1))
            else:
                # Default to monthly if no valid recurrence type or missing custom interval
                end_date = self.start_date + relativedelta(months=self.occurrences)
        else:
            # Default end date if neither end_date nor occurrences is specified
            end_date = date(date.today().year + 5, 12, 31)  # 5 years from now

        while current_date <= end_date:
            # Check if there's an exception for this date
            if current_date in exceptions:
                amount = exceptions[current_date]
                regular_amount = self.amount
            else:
                amount = self.amount if current_date >= reference_date else self._get_historical_amount(current_date)
                regular_amount = amount
            
            if self.recurrence_type == RecurrenceType.CUSTOM:
                # Ensure custom_days has a valid value
                custom_days = self.custom_days if self.custom_days else 1
                current_date = current_date.replace(
                    day=min(custom_days, 
                           calendar.monthrange(current_date.year, current_date.month)[1])
                )
            
            occurrences.append({
                'date': current_date,
                'amount': amount,
                'title': self.title,
                'tag': self.tag,
                'is_exception': current_date in exceptions,
                'id': self.id,
                'regular_amount': regular_amount
            })
            
            if self.recurrence_type == RecurrenceType.MONTHLY:
                current_date += relativedelta(months=1)
            elif self.recurrence_type == RecurrenceType.QUARTERLY:
                current_date += relativedelta(months=3)
            elif self.recurrence_type == RecurrenceType.HALF_YEARLY:
                current_date += relativedelta(months=6)
            elif self.recurrence_type == RecurrenceType.YEARLY:
                current_date += relativedelta(years=1)
            elif self.recurrence_type == RecurrenceType.CUSTOM:
                # Use default interval of 1 month if not specified
                interval = self.custom_months_interval if self.custom_months_interval else 1
                current_date += relativedelta(months=interval)
            else:
                # Default to monthly if no valid recurrence type
                current_date += relativedelta(months=1)
        
        return occurrences
    
    def _get_historical_amount(self, date):
        # Get the historical amount that was effective on the given date
        historical_amount = self.history.filter(
            effective_date__lte=date
        ).order_by('-effective_date').first()
        
        return historical_amount.amount if historical_amount else self.amount

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
    end_date = models.DateField(null=True, blank=True)
    tag = models.CharField(max_length=50, blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    def get_occurrences(self, reference_date=None):
        occurrences = []
        reference_date = reference_date or date.today()
        
        if not self.is_recurring:
            return [{
                'date': self.date,
                'amount': self.amount,
                'title': self.title,
                'tag': self.tag,
                'is_exception': False,
                'id': self.id,
                'regular_amount': self.amount
            }]
        
        current_date = self.date
        end_date = self.end_date or date(date.today().year + 5, 12, 31)
        
        # Get all exceptions for this income
        exceptions = {ex.date: ex.amount for ex in self.exceptions.all()}
        
        while current_date <= end_date:
            # Check if there's an exception for this date
            if current_date in exceptions:
                amount = exceptions[current_date]
                regular_amount = self.amount
            else:
                amount = self.amount if current_date >= reference_date else self._get_historical_amount(current_date)
                regular_amount = amount
            
            occurrences.append({
                'date': current_date,
                'amount': amount,
                'title': self.title,
                'tag': self.tag,
                'is_exception': current_date in exceptions,
                'id': self.id,
                'regular_amount': regular_amount
            })
            
            if self.recurrence_type == RecurrenceType.MONTHLY:
                current_date += relativedelta(months=1)
            elif self.recurrence_type == RecurrenceType.QUARTERLY:
                current_date += relativedelta(months=3)
            elif self.recurrence_type == RecurrenceType.HALF_YEARLY:
                current_date += relativedelta(months=6)
            elif self.recurrence_type == RecurrenceType.YEARLY:
                current_date += relativedelta(years=1)
            else:
                # Default to monthly if no valid recurrence type
                current_date += relativedelta(months=1)
        
        return occurrences

    def _get_historical_amount(self, date):
        # Get the historical amount that was effective on the given date
        historical_amount = self.history.filter(
            effective_date__lte=date
        ).order_by('-effective_date').first()
        
        return historical_amount.amount if historical_amount else self.amount

class ExpenseHistory(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='history')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    changed_date = models.DateTimeField(auto_now_add=True)
    effective_date = models.DateField()
    
    class Meta:
        ordering = ['-changed_date']

class IncomeHistory(models.Model):
    income = models.ForeignKey(Income, on_delete=models.CASCADE, related_name='history')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    changed_date = models.DateTimeField(auto_now_add=True)
    effective_date = models.DateField()
    
    class Meta:
        ordering = ['-changed_date']

class ExpenseException(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='exceptions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    reason = models.CharField(max_length=200, blank=True)
    original_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ['expense', 'date']
        ordering = ['date']
    
    def save(self, *args, **kwargs):
        if not self.original_date:
            self.original_date = self.date
        super().save(*args, **kwargs)

class IncomeException(models.Model):
    income = models.ForeignKey(Income, on_delete=models.CASCADE, related_name='exceptions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    reason = models.CharField(max_length=200, blank=True)
    original_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ['income', 'date']
        ordering = ['date']
    
    def save(self, *args, **kwargs):
        if not self.original_date:
            self.original_date = self.date
        super().save(*args, **kwargs) 