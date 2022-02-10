from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from apps.sgdapi.models import Documento

class DocumentoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        exclude = ('fechaSubida','extension',)

class DocumentoObtenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        exclude = ('fechaSubida','extension','documento_file','nombreDocumento',)
