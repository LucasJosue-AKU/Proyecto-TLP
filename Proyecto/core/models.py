from django.db import models
from api.models import Libro
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    favoritos = models.ManyToManyField(Libro, blank=True)
    related_name = 'perfil'
