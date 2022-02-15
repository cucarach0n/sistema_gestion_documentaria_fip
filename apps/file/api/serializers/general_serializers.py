from rest_framework import serializers
from apps.file.models import *

class File_Serializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
class UnidadArea_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadArea
        fields = '__all__'
class FileInFolder_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FileInFolder
        fields = '__all__'
class FileTag_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FileTag
        fields = '__all__'


