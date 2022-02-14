from msilib.schema import File
from rest_framework import serializers
from apps.sgdapi.models import File

class ContrasenaReinicioActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('id',)