from django.db import models

class Libro(models.Model):
    Titulo = models.CharField(max_length=200)
    Descripcion = models.TextField()
    Categoria = models.TextField(max_length=200)
    Año = models.PositiveIntegerField()
    Autor = models.CharField(max_length=200)
    Paginas = models.PositiveIntegerField()
#todo lo que tiene los libros

    def __str__(self):
        return self.Titulo
