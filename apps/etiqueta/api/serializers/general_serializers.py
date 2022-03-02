import re
from rest_framework import serializers
from apps.etiqueta.models import Etiqueta

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model= Etiqueta
        fields = "__all__"