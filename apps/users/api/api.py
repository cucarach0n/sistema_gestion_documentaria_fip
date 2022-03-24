from apps.folder.models import Folder, FolderInFolder
from apps.users.models import Contrasena_reinicio
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.models import User
from apps.users.api.serializers.user_serializers import UserSerializer,UserCreateSerializer,UserDeleteSerializer
from apps.users.api.serializers.general_serializers import Contrasena_reinicioSerializer
from apps.users.api.serializers.contrasenaReinicio_serializer import ContrasenaReinicioActivateSerializer
from rest_framework import status
from rest_framework import generics
from apps.base.util import send_email
from datetime import datetime
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import FileResponse
from apps.users.authenticacion_mixings import Authentication

class verAvatar(Authentication,APIView):
    
    def get(self,request,avatar=None):
        print(avatar)
        usuario = User.objects.filter(avatar = avatar ).first()
        if usuario:
            pic = usuario.avatar#56 en linux / 34 windows
            file_location =  settings.MEDIA_ROOT +"avatars/"+pic.name 
            file_location = file_location.replace("\\","/")
            
            print('Obteniendo foto de ' + file_location)
            try:    
                #with open(file_location, 'r') as f:
                #    file_data = f.read()
                file_data = open(file_location, 'rb')
                # sending response 
                response = FileResponse(file_data, content_type='image/jpeg')

                
                response['Content-Disposition'] = 'inline'#56 en linux/ 34 windows
            except:
                # handle file not exist case here
                response = Response({'error':'Hubo un error al obtener la foto'},status = status.HTTP_400_BAD_REQUEST)
            return response
        return Response({'error':'No existe la foto solicitada'},status = status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    def get(self,request):
        users = User.objects.all()
        users_serializer = UserSerializer(users,many = True)
        return Response(users_serializer.data, status = status.HTTP_200_OK )
def createCarpetaPrivadaUser(unidadAreaId,user):
    #folderMaster = Folder.objects.filter(carpeta_hija__isnull =True,unidadArea_id = unidadAreaId).first()

    folderHijoPrivado = Folder()
    folderHijoPrivado.slug = get_random_string(11)
    folderHijoPrivado.nombre = "Carpeta privada de {0} {1}.".format(user.name[0:1].upper()+user.name[1:].lower(),user.last_name[0:1].upper())
    folderHijoPrivado.unidadArea_id = unidadAreaId
    folderHijoPrivado.scope = False
    folderHijoPrivado.user_id = user.id
    folderHijoPrivado.save()

    '''folderInFolder = FolderInFolder()
    folderInFolder.child_folder_name = folderHijoPrivado.nombre
    folderInFolder.child_folder_id = folderHijoPrivado.id
    folderInFolder.parent_folder_id = folderMaster.id
    folderInFolder.save()''' 
class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    def post(self,request):
        serializer = self.serializer_class(data = request.data,context = request.data)
        if serializer.is_valid():
            current_site = get_current_site(request).domain
            '''fs = FileSystemStorage(location= settings.MEDIA_ROOT +'avatars/')
            file = fs.save(request.FILES['avatar'].name.replace(" ","_"),request.FILES['avatar'])
            fileurl = fs.url(file)
            print(fileurl)
            doc = fileurl[1:]
            serializer.validated_data['avatar'] = doc'''
            user = serializer.save()

            #absURl = 'http://'+current_site+'/media/avatars'+ doc
            #absURl = 'avatars/'+ doc
            datos = {'correo':user.correo,
                    'token':get_random_string(length=40),
                    'fechaCambio':datetime.today().strftime('%Y-%m-%d'),
                    'estado':1,
                    'usuario':user.id
                    }
            contrasena_reinicioO = Contrasena_reinicioSerializer(data = datos)
            
            if contrasena_reinicioO.is_valid():
                userSendEmail = contrasena_reinicioO.save()
                
                absurl = 'https://'+current_site+'/usuario/validar/'+userSendEmail.token
                #enviar email
                #send_email({'email':'devalo19@gmail.com','domain': str(absurl)})
            userCreadoSerializer = UserSerializer(user)
            if user.is_staff < 3:
                createCarpetaPrivadaUser(user.unidadArea_id,user)
            return Response(userCreadoSerializer.data,status = status.HTTP_200_OK)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class userActivateRetrieveAPIView(APIView):
    serializer_class = ContrasenaReinicioActivateSerializer
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(estado = 1)

    def get(self,request,token=None):
        Contrasena_reinicioUpdate = Contrasena_reinicio.objects.filter(token = token,estado = 1).first()
        if Contrasena_reinicioUpdate: 
            user = User.objects.filter(correo = Contrasena_reinicioUpdate.correo).first()
            if user:
                Contrasena_reinicioUpdate.estado = 0
                user.estado = 1
                user.is_active = True
                Contrasena_reinicioUpdate.save()
                user.save()
                return Response({'Mensaje':'Usuario validado correctamente'},status = status.HTTP_200_OK)
                
            else:
                return Response({'Error':'No se pudo validar dicha informacion'},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Error':'No se pudo validar dicha informacion'},status = status.HTTP_400_BAD_REQUEST)

class userDeleteAPIView(Authentication,generics.DestroyAPIView):
    serializer_class = UserDeleteSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(id = pk).first()
    
    def delete(self,request,pk = None):
        userSerializer = self.get_serializer(data = request.data)
        if userSerializer.is_valid():
            if self.userFull.is_superuser:
                userDeleteResult = self.get_queryset(pk)
                userDeleteResult.delete()
                return Response({'Mensaje':'Usuario eliminado correctamente'},status = status.HTTP_200_OK)
            else:
                return Response({'Error':'No tiene permitido realizar esta accion'},status = status.HTTP_400_BAD_REQUEST)  
        else:
            return Response(userSerializer.errors,status = status.HTTP_400_BAD_REQUEST) 



