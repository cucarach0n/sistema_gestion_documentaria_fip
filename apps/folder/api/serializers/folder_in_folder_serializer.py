from email.policy import default
from apps.folder.api.serializers.general_serializer import Folder_Serializer
from rest_framework import serializers
from apps.folder.models import FolderInFolder,Folder

class FolderInFolderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderInFolder
        exclude = ('id','fechaUpdate','fechaCreacion','slug')

class FolderInFolderValidateCreateSerializer(serializers.Serializer):
    #nombreUsuario = serializers.CharField(max_length = 200)
    child_folder_name = serializers.CharField(max_length=250)
    padreSlug = serializers.CharField(max_length=11)
    publico = serializers.BooleanField(default = True)

    def validate_child_folder_name(self,value):
        padre = FolderInFolder.objects.filter(child_folder_name  = value, parent_folder =Folder.objects.filter(slug = self.context['padreSlug']).first()).first()        
        if padre is None:
            return value
        else:
            raise serializers.ValidationError('Error, ya esiste este subdirectorio')
    def validate(self,data):
        #if data['nombreUsuario'] in data['contrasena']:
        #    raise serializers.ValidationError('El nombre de usuario no puede ser igual a la contrasena')
        #print('Folder validado')
        return data
class FolderInFolderSerializer(serializers.ModelSerializer):
    #parent_folder = Folder_Serializer()
    class Meta:
        model = FolderInFolder
        fields = "__all__"
    def to_representation(self,instance):
        folder = Folder_Serializer(Folder.objects.filter(id = instance.child_folder_id),many = True)

        return {
            'parent_folder': folder.data
        }


