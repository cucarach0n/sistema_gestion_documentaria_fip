# -*- coding: utf-8 -*-
from rest_framework import serializers

class DiskSerializer(serializers.Serializer):
    espacioTotal = serializers.CharField()
    espacioLibre = serializers.CharField()
    espacioUtilizado = serializers.CharField()
    espacioUtilizadoPorcentaje = serializers.CharField()
    unidadMedida = serializers.CharField()