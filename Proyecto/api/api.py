from api.models import Libro
from rest_framework import viewsets, permissions, authentication
from .serializers import ProjectSerializers 

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    #mostrar todos los objetos de models

    permission_classes = [permissions.AllowAny]
    #ignora el texto de despues, le voy a meter autenticacion
    #los permisos, cambiar el AllowAny si no quieres que cualquien aplicacion cliente pueda consultar el servidor
    
    serializer_class = ProjectSerializers