import os
import shutil

def create_directory_structure():
    # Project root structure
    directories = [
        'expense_manager',
        'expenses',
        'expenses/migrations',
        'expenses/templates/expenses',
        'static/css',
        'static/js',
        'static/images',
        'media',
        'templates'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join(directory, '__init__.py'), 'w') as f:
            pass
    
    # Create necessary files
    files = {
        'manage.py': '',
        'requirements.txt': '',
        '.env': '',
        '.gitignore': '',
        'expense_manager/settings.py': '',
        'expense_manager/urls.py': '',
        'expense_manager/wsgi.py': '',
        'expenses/admin.py': '',
        'expenses/apps.py': '',
        'expenses/forms.py': '',
        'expenses/models.py': '',
        'expenses/views.py': '',
        'templates/base.html': '',
    }
    
    for file_path, content in files.items():
        with open(file_path, 'w') as f:
            f.write(content)

if __name__ == '__main__':
    create_directory_structure() 