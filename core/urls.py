"""
Configuración de URLs para la aplicación Core.
Define las rutas principales del sitio.
"""
from django.urls import path
from . import views

# Namespace de la aplicación
app_name = 'core'

urlpatterns = [
    # Página de inicio
    path('', views.HomeView.as_view(), name='home'),
    # Página Acerca de
    path('about/', views.AboutView.as_view(), name='about'),
]
