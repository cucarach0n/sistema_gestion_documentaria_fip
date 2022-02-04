from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from apps.sgdapi.models import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
    
    def validate_nombreUsuario(self,value):
        return value
    def validate_correo(self,value):
        print('validando correo')
        if 'uni.pe' not in value:
            raise serializers.ValidationError('Error, el correo no es valido para esta institucion')
        return value
    def validate_password(self,value):
        if self.context['nombreUsuario'] == value:
            raise serializers.ValidationError('La contrasena no puede ser igual al nombre de usuario')
        return value
    def validate_avatar(self,value):
        return value
    def validate_estado(self,value):
        print('validando estado')
        if value == 1:
            raise serializers.ValidationError('Error, estado no valido')
        return value
    def validate_fechaCreacion(self,value):
        
        return value
    def validate_fechaActualizacion(self,value):
        return value
    def validate(self,data):
        #if data['nombreUsuario'] in data['contrasena']:
        #    raise serializers.ValidationError('El nombre de usuario no puede ser igual a la contrasena')
        print('Usuario validado')
        return data
    
    def create(self,validated_data):
        usuario = Usuario(**validated_data)
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario
    
    def update(self,instance,validated_data):
        usuario_actualisado = super().update(instance,validated_data)

        usuario_actualisado.set_password(validated_data['password'])
        usuario_actualisado.save()
        return usuario_actualisado
    
    '''
    def to_representation(self,instance):
        #data = super().to_representation(instance)
        #print(data)
        return{
            'id': instance['id'],
            'nombreUsuario': instance['nombreUsuario'],
            'correo': instance['correo'],
            'password': instance['password'],
            'avatar': instance['avatar'],
            'estado': instance['estado'],
            'fechaCreacion': instance['fechaCreacion'],
            'fechaActualizacion': instance['fechaActualizacion']
        }
    '''
class UsuarioEmailSerializer(serializers.Serializer):
    #nombreUsuario = serializers.CharField(max_length = 200)
    correo = serializers.EmailField()
    fechaCambio = serializers.DateField('actualizacion')
    token = serializers.CharField(max_length=40)

    #def validate_nombreUsuario(self,value):
        #print(self.context)
        #print('usuario validado')
    #    return value  
    def validate_correo(self,value):
        #print('correo validado')
        return value
    def validate_fechaCambio(self,value):
        #print('fecha validado')
        return value
    def validate_token(self,value):
        #print('fecha validado')
        return value
    def validate(self,data):
        #print('email enviado')
        return data
    def create(self,validated_data):
        return Contrasena_reinicio.objects.create(**validated_data)


class Contrasena_reinicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrasena_reinicio
        fields = '__all__'
    def validate_correo(self,value):
        return value
    def validate_token(self,value):
        return value
    def validate_fechaCambio(self,value):
        return value
    def validate_estado(self,value):
        return value
    def validate(self,data):
        return data