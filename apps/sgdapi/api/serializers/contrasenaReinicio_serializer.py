from rest_framework import serializers
from apps.sgdapi.models import Documento

class ContrasenaReinicioActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        exclude = ('id',)