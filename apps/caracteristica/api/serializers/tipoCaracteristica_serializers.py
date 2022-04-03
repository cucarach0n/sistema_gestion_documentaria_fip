from apps.caracteristica.api.serializers.caracteristica_serializers import CaracteristicaListSerializer
from rest_framework import serializers
from apps.caracteristica.models import Caracteristica, TipoCaracteristica
from apps.file.models import File
class TipoCaracteristicaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCaracteristica
        fields = ['nombreTipo']
class TipoCaracteristicaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCaracteristica
        fields = ['id','nombreTipo']
    def to_representation(self,instance):
        caracteristicas = Caracteristica.objects.filter(tipoCaracteristica_id = instance.id)
        return {
            'id': instance.id,
            'nombreTipo': instance.nombreTipo,
            'caracteristicas': CaracteristicaListSerializer(caracteristicas,many=True).data
        }