# myapp/templatetags/language_switcher.py
from django import template
from django.urls import resolve, reverse
from django.utils.translation import get_language

register = template.Library()

@register.simple_tag(takes_context=True)
def switch_language(context, lang_code):
    request = context['request']
    url_name = resolve(request.path_info).url_name
    current_language = get_language()

    # Remove the current language code from the URL path
    current_path = request.path_info.replace(f'/{current_language}/', '/', 1)
    # Construct the new path with the new language code
    new_path = f'/{lang_code}{current_path}'

    return new_path
