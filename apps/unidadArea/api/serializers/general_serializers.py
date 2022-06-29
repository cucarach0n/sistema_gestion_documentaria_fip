from rest_framework import serializers
from apps.unidadArea.models import *

class UnidadArea_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadArea
        fields = '__all__'
