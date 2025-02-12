from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_expense_custom_months_interval_expense_last_modified_and_more'),  # This should be your last migration
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
    ] 