from django import template
from django.utils.html import mark_safe

register = template.Library()

@register.filter
def waypoint(number):
    if number == 0 or number == 1:
        return False
    result = number % 50
    return True if result == 0 else False
