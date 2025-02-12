from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('expenses', 'previous_migration'),
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