from rest_framework import serializers
from apps.file.models import File

class FileEmailShareSerializer(serializers.Serializer):
    fileSlug = serializers.CharField()
    asunto = serializers.CharField()
    mensaje = serializers.CharField()
    emailDestino = serializers.EmailField()
    def validate_fileSlug(self,value):
        for slug in value.split(','):
            file = File.objects.filter(slug = slug).first()
            if file is None:
                raise serializers.ValidationError("No existe el archivo")
        #fileTag = FileTag.objects.filter(file = File.objects.filter(slug = value).first(), tag_id = self.context['tagId']).first()
        return value.split(',')

