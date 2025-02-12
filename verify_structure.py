import os

def check_structure():
    required_files = [
        'manage.py',
        'requirements.txt',
        '.env',
        '.gitignore',
        'expense_manager/settings.py',
        'expense_manager/urls.py',
        'expense_manager/wsgi.py',
        'expenses/admin.py',
        'expenses/apps.py',
        'expenses/forms.py',
        'expenses/models.py',
        'expenses/views.py',
        'expenses/templates/expenses/base.html',
        'expenses/templates/expenses/dashboard.html',
        'expenses/templates/expenses/expense_form.html',
        'expenses/templates/expenses/expense_list.html',
        'expenses/templates/expenses/income_form.html',
        'expenses/templates/expenses/income_list.html',
        'expenses/templates/expenses/month_detail.html',
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"Missing: {file_path}")
        else:
            print(f"Found: {file_path}")

    # Check directories
    required_dirs = [
        'static/css',
        'static/js',
        'static/images',
        'media',
        'expenses/migrations',
    ]
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"Missing directory: {dir_path}")
        else:
            print(f"Found directory: {dir_path}")

if __name__ == "__main__":
    check_structure() 