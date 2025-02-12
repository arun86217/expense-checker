import os

def create_static_structure():
    # Create static directories
    static_dirs = [
        'static/css',
        'static/js',
        'static/images',
        'staticfiles',
        'media'
    ]
    
    for directory in static_dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create initial CSS file
    css_content = """
/* Custom styles */
.navbar {
    margin-bottom: 20px;
}
"""
    with open('static/css/style.css', 'w') as f:
        f.write(css_content)
    print("Created: static/css/style.css")

if __name__ == "__main__":
    create_static_structure() 