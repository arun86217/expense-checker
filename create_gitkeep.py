import os

def create_gitkeep():
    directories = [
        'static/css',
        'static/js',
        'static/images',
        'media'
    ]
    
    for directory in directories:
        gitkeep_path = os.path.join(directory, '.gitkeep')
        with open(gitkeep_path, 'w') as f:
            pass
        print(f"Created: {gitkeep_path}")

if __name__ == "__main__":
    create_gitkeep() 