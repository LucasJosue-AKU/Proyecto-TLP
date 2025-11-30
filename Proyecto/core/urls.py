from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('catalogo/', views.catalogo, name="Catalogo"),
    path('catalogo/<int:id>', views.informacion, name="Informacion"),
    path('registro/', views.registro, name="Registro"),
    path('inicio-sesion/', views.inicio_sesion, name="Inicio-sesion"),
]