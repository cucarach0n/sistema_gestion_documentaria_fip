from rest_framework import serializers
from apps.file.models import FileTag,File

class FileTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileTag
        exclude = ('id','fechaRegistro','fechaUpdate',)
class FileTagCreateSerializer(serializers.Serializer):
    documentoSlug = serializers.CharField(max_length = 10)
    tagId = serializers.CharField()
    
    def validate_documentoSlug(self,value):
        fileTag = FileTag.objects.filter(file = File.objects.filter(slug = value).first(), tag_id = self.context['tagId']).first()
        if fileTag:
            raise serializers.ValidationError("Ya existe este tag en el file")
        return value
    def create(self,validated_data):
        file = File.objects.filter(slug = validated_data['documentoSlug']).first()
        fileTag = FileTag(file = file,tag_id = validated_data['tagId'])
        fileTag.save()
        return fileTag

class FileTagDeleteSerializer(serializers.Serializer):
    documentoSlug = serializers.CharField(max_length = 10)
    tagId = serializers.CharField()
    
    def validate_documentoSlug(self,value):
        fileTag = FileTag.objects.filter(file = File.objects.filter(slug = value).first()).first()
        if fileTag is None:
            raise serializers.ValidationError("No existe el archivo en el tag")
        return value
    def validate_documentoSlug(self,value):
        fileTag = FileTag.objects.filter(tag_id = self.context['tagId']).first()
        if fileTag is None:
            raise serializers.ValidationError("No existe el tag en el archivo")
        return value
    def delete(self):
        fileTag = FileTag.objects.filter(file = File.objects.filter(slug = self.context['documentoSlug']).first(), tag_id = self.context['tagId']).first()
        fileDelete = fileTag.delete()
        return fileDelete


