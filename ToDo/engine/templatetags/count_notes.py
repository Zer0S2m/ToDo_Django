from django import template


register = template.Library()

@register.filter
def get_count_notes(dictionary, key):
    return dictionary.get(key)
