from rest_framework import serializers
from apps.sgdapi.models import *


class Contrasena_reinicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrasena_reinicio
        fields = '__all__'
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
class TipoGestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoGestion
        fields = '__all__'

class Tipo_carpetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_carpeta
        fields = '__all__'

class SubCarpetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCarpeta
        fields = '__all__'

class UnidadDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadDocumento
        fields = '__all__'

class AreaDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaDocumento
        fields = '__all__'

class CarpetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carpeta
        fields = '__all__'

class PropiedadDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropiedadDocumento
        fields = '__all__'

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'

class DocumentoOcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoOcr
        fields = '__all__'



