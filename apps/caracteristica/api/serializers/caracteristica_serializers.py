from rest_framework import serializers
from apps.caracteristica.models import Caracteristica, CaracteristicaFile, TipoCaracteristica
from apps.file.models import File
class CaracteristicaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristica
        fields = ['nombreCaracteristica','tipoCaracteristica']
    def to_representation(self,instance):
        tipoCaracteristica = TipoCaracteristica.objects.get(id = instance.tipoCaracteristica_id)
        return {
            'id': instance.id,
            'nombreCaracteristica': instance.nombreCaracteristica,
            'tipoCaracteristica': tipoCaracteristica.nombreTipo
        }
class CaracteristicaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristica
        fields = ['id','nombreCaracteristica','tipoCaracteristica']
    def to_representation(self,instance):
        tipoCaracteristica = TipoCaracteristica.objects.get(id = instance.tipoCaracteristica_id)
        return {
            'id': instance.id,
            'nombreCaracteristica': instance.nombreCaracteristica,
            'tipoCaracteristica': tipoCaracteristica.nombreTipo
        }
class CaracteristicaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristica
        fields = ['id','nombreCaracteristica','tipoCaracteristica']
    def to_representation(self,instance):
        return {
            'id': instance.id,
            'nombreCaracteristica': instance.nombreCaracteristica
        }

