from django.db import connection

def verify_database():
    with connection.cursor() as cursor:
        # Get all tables
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name LIKE 'expenses_%';
        """)
        tables = cursor.fetchall()
        print("Found tables:", tables)
        
        # Check expenses table structure
        cursor.execute("PRAGMA table_info(expenses_expense);")
        expense_columns = cursor.fetchall()
        print("\nExpense table columns:", expense_columns)
        
        # Check income table structure
        cursor.execute("PRAGMA table_info(expenses_income);")
        income_columns = cursor.fetchall()
        print("\nIncome table columns:", income_columns)

if __name__ == "__main__":
    verify_database() 