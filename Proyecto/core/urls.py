from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('catalogo/', views.catalogo, name="Catalogo"),
]