"""
Configuración de URLs para el proyecto reflex-docs.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # URLs de la aplicación Core (página de inicio y páginas principales)
    path('', include('core.urls')),
]
