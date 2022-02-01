from django.contrib import admin
from django.urls import path
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("engine.urls")),
    path("accounts/", include("accounts.urls")),
]

handler404 = "ToDo.views.page_not_found_view"
