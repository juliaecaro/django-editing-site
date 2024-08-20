# templatetags/format_filters.py
from django import template
from media_files.utils import format_count

register = template.Library()

@register.filter(name='format_count_filter')
def format_count_filter(value):
    try:
        return format_count(int(value))
    except (ValueError, TypeError):
        return value