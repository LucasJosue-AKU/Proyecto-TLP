from django.db import models

class Libro(models.Model):
    Titulo = models.CharField(max_length=200)
    Descripcion = models.TextField()
    Fecha = models.DateField
    Portada = models.URLField(max_length=500)
    Autor = models.CharField(max_length=200)
    Paginas = models.PositiveIntegerField()
#todo lo que tiene los libros
