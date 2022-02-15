from rest_framework import serializers
from apps.folder.models import *

class Folder_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'
class FolderInFolder_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FolderInFolder
        fields = '__all__'