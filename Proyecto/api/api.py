from api.models import Libro
from rest_framework import viewsets, permissions, authentication
from .serializers import ProjectSerializers 
from .permiso import Admin_o_Usuario

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    
    serializer_class = ProjectSerializers

    
    permission_classes = [Admin_o_Usuario]
    #ignora el texto de despues, le voy a meter autenticacion
    #los permisos, cambiar el AllowAny si no quieres que cualquien aplicacion cliente pueda consultar el servidor

    #mostrar todos los objetos de models
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    #creando las autenticaciones token es ideal para celulares y session es ideal para pagina web de django
