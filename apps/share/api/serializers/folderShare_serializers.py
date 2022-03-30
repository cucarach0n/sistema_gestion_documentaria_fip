from multiprocessing.sharedctypes import Value
from apps.base.util import validarPrivado
from apps.folder.models import Folder, FolderInFolder
from apps.users.models import User
from rest_framework import serializers
from apps.share.models import FolderShare

class FolderShareCreateSerializer(serializers.Serializer):
    #history_id = serializers.CharField()
    slugFolder = serializers.CharField()
    correoTo = serializers.CharField()
    def validate_correoTo(self,value):
        userResult = User.objects.filter(correo = value).first()
        if userResult:
            if not userResult.id == int(self.context['userId']):
                return userResult.id
            elif userResult.id == int(self.context['userId']):
                raise serializers.ValidationError('Seleccione otro usuario a enviar el folder')
            elif userResult.unidadArea_id == self.context['unidadId']:
                raise serializers.ValidationError('No se puede compartir con usuarios de la misma unidad')
        raise serializers.ValidationError('El usuario a compartir no existe!')        
        
    def validate_slugFolder(self,value):
        folderResult = Folder.objects.filter(slug=value, unidadArea_id = self.context['unidadId'],eliminado = False).first()
        if folderResult:
            
            if validarPrivado(folderResult,self.context['userId']):
                raise serializers.ValidationError('La carpeta es privada , no se puede compartir') 
            elif not FolderInFolder.objects.filter(child_folder_id = folderResult.id):
                raise serializers.ValidationError('Esta carpeta no se puede compartir')
            elif FolderShare.objects.filter(estado=True, userTo_id = User.objects.get(correo=self.context['userTo']).id, folder_id = folderResult.id):
                raise serializers.ValidationError('La carpeta ya se encuentra compartida')
            return folderResult.id
        
        raise serializers.ValidationError('No existe la carpeta')  
class FolderShareValidateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderShare
        fields = ['userFrom','userTo','folder']
class FolderShareClonarSerializer(serializers.Serializer):
    slugFolder = serializers.CharField()
    def validate_slugFolder(self,value):
        return value
    class Meta:
        model = Folder
        