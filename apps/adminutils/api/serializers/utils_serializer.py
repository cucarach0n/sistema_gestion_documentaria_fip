# -*- coding: utf-8 -*-
from rest_framework import serializers

class CuentasSerializer(serializers.Serializer):
    carpetas = serializers.CharField()
    files = serializers.CharField()
    usuarios = serializers.CharField()
    gestiones = serializers.CharField()
    categorias = serializers.CharField()