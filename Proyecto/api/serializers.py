from rest_framework import serializers
from .models import Libro

class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ('id','Titulo','Descripcion','Fecha','Autor','Paginas')
        #definiendo todo lo que necesita serializer, para entender models de python