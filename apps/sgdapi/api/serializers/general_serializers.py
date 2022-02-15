from rest_framework import serializers
from apps.sgdapi.models import *


class Contrasena_reinicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrasena_reinicio
        fields = '__all__'

'''class Tag_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'''

'''class Folder_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'
class FolderInFolder_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FolderInFolder
        fields = '__all__'''
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


