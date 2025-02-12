from django.db import migrations

def populate_original_dates(apps, schema_editor):
    ExpenseException = apps.get_model('expenses', 'ExpenseException')
    IncomeException = apps.get_model('expenses', 'IncomeException')
    
    for exception in ExpenseException.objects.all():
        if not exception.original_date:
            exception.original_date = exception.date
            exception.save()
    
    for exception in IncomeException.objects.all():
        if not exception.original_date:
            exception.original_date = exception.date
            exception.save()

def reverse_populate(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('expenses', '0002_expenseexception_original_date_incomeexception_original_date'),  # This should match your previous migration name
    ]

    operations = [
        migrations.RunPython(populate_original_dates, reverse_populate),
    ] 