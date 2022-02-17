from rest_framework import serializers
from apps.unidadArea.models import *

class UnidadAreaList_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadArea
        exclude = ('id',)
        
class UnidadAreaCreate_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadArea
        exclude = ('id',)

