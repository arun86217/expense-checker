from django import template
from expenses.utils import format_indian_currency

register = template.Library()

@register.filter
def indian_currency(amount):
    return format_indian_currency(amount) 