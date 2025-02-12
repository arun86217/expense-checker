from django.utils import timezone
from datetime import date
from expenses.models import Expense, Income

# Create test expenses
test_expenses = [
    {
        'title': 'Rent',
        'amount': 1000,
        'start_date': date(2024, 1, 1),
        'end_date': date(2024, 12, 31),
        'recurrence_type': 'monthly',
        'tag': 'Housing'
    },
    {
        'title': 'Internet',
        'amount': 50,
        'start_date': date(2024, 1, 1),
        'end_date': date(2024, 12, 31),
        'recurrence_type': 'monthly',
        'tag': 'Utilities'
    }
]

# Create test incomes
test_incomes = [
    {
        'title': 'Salary',
        'amount': 5000,
        'date': date(2024, 1, 1),
        'is_recurring': True,
        'recurrence_type': 'monthly',
        'tag': 'Employment'
    },
    {
        'title': 'Freelance',
        'amount': 1000,
        'date': date(2024, 1, 15),
        'is_recurring': False,
        'tag': 'Side Income'
    }
]

def create_test_data():
    # Create expenses
    for expense_data in test_expenses:
        Expense.objects.create(**expense_data)
        print(f"Created expense: {expense_data['title']}")
    
    # Create incomes
    for income_data in test_incomes:
        Income.objects.create(**income_data)
        print(f"Created income: {income_data['title']}")

if __name__ == "__main__":
    create_test_data() 