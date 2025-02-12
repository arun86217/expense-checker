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
        ('expenses', '0001_initial'),
    ]

    operations = [
        # Add custom_months_interval field
        migrations.AddField(
            model_name='expense',
            name='custom_months_interval',
            field=models.IntegerField(blank=True, help_text='Number of months between occurrences', null=True),
        ),
        # Add last_modified fields
        migrations.AddField(
            model_name='expense',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='income',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        # Add original_date fields
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
        # Populate original_date values
        migrations.RunPython(populate_original_dates, reverse_populate),
    ] 