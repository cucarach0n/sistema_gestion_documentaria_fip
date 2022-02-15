from rest_framework import serializers
from apps.users.models import Contrasena_reinicio

class ContrasenaReinicioActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrasena_reinicio
        exclude = ('id',)