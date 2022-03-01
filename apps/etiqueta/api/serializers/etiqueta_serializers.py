from apps.file.models import File
from rest_framework import serializers
from apps.etiqueta.models import Etiqueta

class EtiquetaCreateSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length = 45)
    slugFile = serializers.CharField(max_length = 11)

    '''class Meta:
        model = Etiqueta
        exclude = ('user_id','fechaCreacion','fechaUpdate',)'''
    def validate_nombre(self,value):
        fileResult = File.objects.filter(slug = self.context['fileSlug']).first()
        etiquetaResult = Etiqueta.objects.filter(user_id=self.context['userId'],file_id = fileResult.id,nombre = value).first()
        if etiquetaResult is None:
            return value
        else:
            raise serializers.ValidationError('Error, ya creastes esta etiqueta para este file') 
    def validate(self,data):
        return data
        
    def create(self,validated_data):
        fileResult = File.objects.filter(slug = validated_data['slugFile']).first()
        etiqueta = Etiqueta(file_id = fileResult.id,nombre = validated_data['nombre'],user_id = self.context['userId'])
        etiqueta.save()
        return etiqueta     
