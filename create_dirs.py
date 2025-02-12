import os

def create_missing_dirs():
    directories = [
        'static/css',
        'static/js',
        'static/images',
        'media',
        'expenses/migrations',
        'expenses/templates/expenses'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

if __name__ == "__main__":
    create_missing_dirs() 