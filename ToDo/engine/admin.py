from django.contrib import admin

from .models import Note
from .models import Category


admin.site.register(Note)
admin.site.register(Category)
