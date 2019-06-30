from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def minimum(value, arg):
    return min(value, arg)
