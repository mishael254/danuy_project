from django import template

register = template.Library()

@register.filter
def integer_range(value):
    return range(int(value))