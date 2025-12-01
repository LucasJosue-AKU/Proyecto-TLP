from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('catalogo/', views.catalogo, name="Catalogo"),
    path('catalogo/<int:id>', views.informacion, name="Informacion"),
    path('registro/', views.registro, name="Registro"),
    path('inicio-sesion/', views.inicio_sesion, name="Inicio-sesion"),
    path('cerrar-sesion/', views.cerrar_sesion, name="Cerrar-sesion"),
    path('marcar-libro/<int:id>', views.marcar_libro, name="Marcar-libro"),
    path('quitar-marcado/<int:id>', views.quitar_marcado, name="Quitar-marcado"),
]