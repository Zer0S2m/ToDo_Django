from django.contrib import admin

from .models import (
    Note, Category, File
)


admin.site.register(Note)
admin.site.register(Category)
admin.site.register(File)
