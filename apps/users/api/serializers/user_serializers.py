from dataclasses import fields
from rest_framework import serializers
from apps.users.models import User

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['correo','name','last_name','avatar','is_staff','is_superuser']
    def validate_avatar(self,value):
        return value
    def validate(self,data):
        print('usuario token validado!')
        return data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ['name']
        exclude = ('estado','password','groups','user_permissions','last_login',)
    def to_representation(self,instance):
        return {
        "id": instance.id,
        "is_superuser": instance.is_superuser,
        "correo": instance.correo,
        "name": instance.name,
        "last_name": instance.last_name,
        "avatar": instance.avatar.name,
        "is_active": instance.is_active,
        "is_staff": instance.is_staff,
        "idUnidadArea": instance.unidadArea_id,
        "unidadArea": instance.unidadArea.nombreUnidad
    }
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('id','estado','last_login','is_superuser','is_active','groups','user_permissions','avatar',)                
    def validate_correo(self, value):
        if '@fip.uni.edu.pe' not in value:
            raise serializers.ValidationError('Error, el correo no es valido para esta institucion')
        return value
    def validate(self,data):
        #if data['nombreUsuario'] in data['contrasena']:
        #    raise serializers.ValidationError('El nombre de usuario no puede ser igual a la contrasena')
        return data
    def create(self,validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self,instance,validated_data):
        user_actualisado = super().update(instance,validated_data)

        user_actualisado.set_password(validated_data['password'])
        user_actualisado.save()
        return user_actualisado
class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']