from rest_framework import serializers
from apps.users.models import *

class Contrasena_reinicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrasena_reinicio
        fields = '__all__'