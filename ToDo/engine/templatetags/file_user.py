from django import template

from ..models import Note


register = template.Library()

@register.filter
def get_name_file_user(dictionary, path):
    path_split = path.split("/")
    return path_split[-1]


@register.filter
def get_files_user(dictionary, request):
    id_note = int([i for i in request.path.split("/") if i][-1])

    files = Note.objects.get(
        user = request.user,
        id = id_note
    ).files.all()
    
    return files
