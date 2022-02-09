from django import template


register = template.Library()

@register.filter
def get_name_file_user(dictionary, path):
    path_split = path.split("/")
    return path_split[-1]
