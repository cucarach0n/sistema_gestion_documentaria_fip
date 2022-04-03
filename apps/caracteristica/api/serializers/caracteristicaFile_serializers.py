from rest_framework import serializers
from apps.caracteristica.models import CaracteristicaFile
from apps.file.models import File
class CaracteristicaFileCreateSerializer(serializers.Serializer):
    slugFile = serializers.CharField(allow_blank=True)
    idCategoria = serializers.IntegerField(allow_null = True)
    class Meta:
        model = CaracteristicaFile
    def validate_slugFile(self,value):
        file = File.objects.get(slug = value)
        if self.Meta.model.objects.filter(file_id = file.id,caracteristica_id = self.context['idCategoria']):
            raise serializers.ValidationError("El archivo ya esta asociado a esta caracteristica")
        return file.id
    def create(self,validated_data):
        caracteristicaFile = self.Meta.model(file_id = validated_data['slugFile'],caracteristica_id = validated_data['idCategoria'])#,unidadArea_id=validated_data['unidadareaid'])
        caracteristicaFile.save()
        return caracteristicaFile
