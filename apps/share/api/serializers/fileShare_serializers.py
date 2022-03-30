from apps.base.util import validarPrivado
from apps.file.models import File
from apps.folder.models import Folder
from apps.users.models import User
from rest_framework import serializers
from apps.share.models import FileShare

class FileShareCreateSerializer(serializers.Serializer):
    #history_id = serializers.CharField()
    slugFile = serializers.CharField()
    correoTo = serializers.CharField()
    def validate_correoTo(self,value):
        userResult = User.objects.filter(correo = value).first()
        if userResult:
            if not userResult.id == int(self.context['userId']):
                return userResult.id
            raise serializers.ValidationError('Seleccione otro usuario a enviar el file') 
        raise serializers.ValidationError('El usuario a compartir no existe!')        
        
    def validate_slugFile(self,value):
        folderPadre = Folder.objects.filter(fileinfolder__file__slug = value,unidadArea_id = self.context['unidadId']).first()
        if folderPadre:
            if validarPrivado(folderPadre,self.context['userId']):
                raise serializers.ValidationError('La carpeta contenedora es privada, no se puede compartir')
            file = File.objects.filter(slug = value,unidadArea_id = self.context['unidadId']).first()
            if file:
                if FileShare.objects.filter(estado=True, userTo_id = User.objects.get(correo=self.context['userTo']).id, file_id = file.id):
                    raise serializers.ValidationError('El file ya se encuentra compartido')
                return file.id
            raise serializers.ValidationError('El documento no existe')
        raise serializers.ValidationError('No existe el file o es privado') 
class FileShareValidateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileShare
        fields = ['userFrom','userTo','file']
        