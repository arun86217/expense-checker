import os

def create_template_files():
    templates = {
        'expenses/templates/expenses/base.html': base_html,
        'expenses/templates/expenses/dashboard.html': dashboard_html,
        'expenses/templates/expenses/expense_form.html': expense_form_html,
        'expenses/templates/expenses/expense_list.html': expense_list_html,
        'expenses/templates/expenses/income_form.html': income_form_html,
        'expenses/templates/expenses/income_list.html': income_list_html,
        'expenses/templates/expenses/month_detail.html': month_detail_html,
    }
    
    for file_path, content in templates.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {file_path}")

if __name__ == "__main__":
    create_template_files() 