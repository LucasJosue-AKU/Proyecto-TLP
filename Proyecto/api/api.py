from api.models import Libro
from rest_framework import viewsets, permissions
from .serializers import ProjectSerializers 
class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    #mostrar todos los objetos de models
    permission_classes = [permissions.AllowAny]
    #los permisos, cambiar el AllowAny si no quieres que cualquien aplicacion cliente pueda consultar el servidor
    serializer_class = ProjectSerializers