from django.db import migrations, models

def populate_original_dates(apps, schema_editor):
    ExpenseException = apps.get_model('expenses', 'ExpenseException')
    IncomeException = apps.get_model('expenses', 'IncomeException')
    
    for exception in ExpenseException.objects.all():
        exception.original_date = exception.date
        exception.save()
    
    for exception in IncomeException.objects.all():
        exception.original_date = exception.date
        exception.save()

def reverse_populate(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('expenses', '0002_expense_custom_months_interval_expense_last_modified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenseexception',
            name='original_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='incomeexception',
            name='original_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.RunPython(populate_original_dates, reverse_populate),
    ] 