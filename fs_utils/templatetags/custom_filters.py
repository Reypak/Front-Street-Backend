from django import template

register = template.Library()


@register.filter(name='stringify')
def stringify(value):
    """Replace underscores with spaces and capitalize words."""
    return value.replace('_', ' ').title()
