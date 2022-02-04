import imp
from json import tool
from multiprocessing import context
from rest_framework import status
from rest_framework.response import Response
#from rest_framework.views import APIView
from rest_framework.decorators import api_view
from apps.sgdapi.models import *
from apps.sgdapi.api.serializers.usuario_serializers import *
from datetime import datetime

from django.utils.crypto import get_random_string

from apps.sgdapi.util import send_email

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
'''
class UsuarioAPIView(APIView):
    def get(self,request):
        usuarios = Usuario.objects.all()
        usuarios_serializer = UsuarioSerializer(usuarios,many = True)
        return Response(usuarios_serializer.data);
'''
@api_view(['GET','POST'])
def usuario_api_view(request):

    #Listar Usuarios
    if request.method == 'GET':
        usuarios = Usuario.objects.all()#.values('id','nombreUsuario','correo','password','avatar','estado','fechaCreacion','fechaActualizacion')
        usuarios_serializer = UsuarioSerializer(usuarios,many = True)
        return Response(usuarios_serializer.data,status = status.HTTP_200_OK );
    #Registrar usuario
    elif request.method == "POST":
        #print(request.data)
        usuario_serializer = UsuarioSerializer(data = request.data, context =  request.data)
        if usuario_serializer.is_valid():
            usuarioSave = usuario_serializer.save()

            #Obteniendo el correo a enviar
            usuarioEmail_serializer = {
                'correo':usuarioSave.correo,
                'fechaCambio' : datetime.today().strftime('%Y-%m-%d'),
                'token' : get_random_string(length=40)
            }

            usuarioEmail_serializer = UsuarioEmailSerializer(data = usuarioEmail_serializer,context = usuarioEmail_serializer )
            if usuarioEmail_serializer.is_valid():
                usuarioEmai_instance = usuarioEmail_serializer.save()
                print(usuarioEmai_instance)
                current_site = get_current_site(request).domain
                aburl = 'http://'+current_site+'/usuario/validar'+'?token='+usuarioEmai_instance.token
                contenidoRenderizado = send_email({'email':'devalo19@gmail.com','domain': str(aburl)})

                print(contenidoRenderizado)
            else:
                print(usuarioEmail_serializer.errors)

            return Response({'message':'Usuario Registrado Correctamente'})
        return Response(usuario_serializer.errors,status = status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def usuario_detail_api_view(request,pk = None):
    print('usuario detail')
    #usuario = Usuario.objects.filter(id = pk).values('id','nombreUsuario','correo','password','avatar','estado','fechaCreacion','fechaActualizacion').first()
    usuario = Usuario.objects.filter(id = pk).first()
    if usuario:
        print('si existe usuario')
        #Buscar 1
        if request.method == 'GET':
            print('obteniendo user...')
            usuario_serializer = UsuarioSerializer(usuario)
            return Response(usuario_serializer.data,status = status.HTTP_200_OK)
        #Actualizar
        elif request.method == 'PUT':
            print('actualizando user...')
            print(usuario)
            usuario_serializer = UsuarioSerializer(usuario,data = request.data, context =  request.data)
            if usuario_serializer.is_valid():
                usuario_serializer.save()
                return Response({'message':'Usuario Actualizado Correctamente'},status = status.HTTP_200_OK);
            return Response(usuario_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        #Eliminar
        elif request.method == 'DELETE':
            usuario.detele()
            return Response({'message':'Usuario Eliminado Correctamente'},status = status.HTTP_200_OK)
    return Response({'message':'No se ha encontrado un usuario con estos datos'},status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def usuario_validacion_api_view(request,token = None):
    if request.method == 'GET':
        contrasena_reinicio = Contrasena_reinicio.objects.filter(token = token,estado =1).first()
        if contrasena_reinicio:
            contrasena_reinicio.estado = 0
            contrasena_reinicio.save()
            return Response({'message':'Usuario validado correctamente'},status = status.HTTP_200_OK)
        else:
            return Response({'message':'Error en la validacion'},status = status.HTTP_400_BAD_REQUEST)
