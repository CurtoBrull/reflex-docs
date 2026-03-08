"""
Vistas para la aplicación Core.
Gestiona las páginas principales del sitio.
"""
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Vista para la página de inicio.
    Muestra la página principal del sitio de documentación de Reflex.
    """
    template_name = 'core/home.html'


class AboutView(TemplateView):
    """
    Vista para la página Acerca de.
    Muestra información sobre el proyecto de documentación de Reflex.
    """
    template_name = 'core/about.html'
