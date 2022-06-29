from apps.folder.models import Folder, FolderInFolder
from apps.users.models import Contrasena_reinicio
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.models import User
from apps.users.api.serializers.user_serializers import UserDisabledSerializer, UserSerializer,UserCreateSerializer,UserDeleteSerializer, UserUpdateSerializer
from apps.users.api.serializers.general_serializers import Contrasena_reinicioSerializer
from apps.users.api.serializers.contrasenaReinicio_serializer import ContrasenaReinicioActivateSerializer
from rest_framework import status
from rest_framework import generics
from apps.base.util import send_email, send_password
from datetime import datetime
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import FileResponse
from apps.users.authenticacion_mixings import Authentication

class verAvatar(Authentication,APIView):
    
    def get(self,request):
        usuario = User.objects.filter(id = self.userFull.id ).first()
        if usuario:
            pic = usuario.avatar#56 en linux / 34 windows
            #file_location =  settings.MEDIA_ROOT +"avatars/"+pic.name 
            file_location =  settings.MEDIA_ROOT +pic.name 
            file_location = file_location.replace("\\","/")
            
            print('Obteniendo foto de ' + usuario.name)
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
        users = User.objects.filter(is_superuser = False)
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
            if user.is_staff < 3:
                createCarpetaPrivadaUser(user.unidadArea_id,user)
            if contrasena_reinicioO.is_valid():
                userSendEmail = contrasena_reinicioO.save()
                
                absurl = 'https://'+current_site+'/usuario/validar/'+userSendEmail.token
                #enviar email
                send_email({'email':user.correo,'domain': str(absurl),'usuario':user,'password':serializer.validated_data['password']})
            userCreadoSerializer = UserSerializer(user)
            
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


    '''def update(self,request,pk = None):
        userSerializer = self.get_serializer(data = request.data)
        if userSerializer.is_valid():
            if self.userFull.is_superuser:
                userResult = self.get_queryset(pk)
                userResult.is_active = False
                userResult.save()
                return Response({'Mensaje':'Usuario inhabilitado correctamente'},status = status.HTTP_200_OK)
            else:
                return Response({'Error':'No tiene permitido realizar esta accion'},status = status.HTTP_400_BAD_REQUEST)  
        else:
            return Response(userSerializer.errors,status = status.HTTP_400_BAD_REQUEST) '''
class userDisabledAPIView(Authentication,generics.UpdateAPIView):
    serializer_class = UserDisabledSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(id = pk).first()

    def put(self,request,pk = None):
        print(request.data)
        userSerializer = self.get_serializer(data = request.data)
        #userResult = self.get_queryset(pk)
        if userSerializer.is_valid():
            if self.userFull.is_superuser:
                mensaje = "inhabilitado"
                print(userSerializer.validated_data)
                userResult = self.get_queryset(request.data['id'])
                userResult.is_active = userSerializer.validated_data['is_active']
                userResult.save()
                if(userResult.is_active):
                    mensaje = "habilitado"
                return Response({'Mensaje':'Usuario {0} correctamente'.format(mensaje)},status = status.HTTP_200_OK)
            else:
                return Response({'Error':'No tiene permitido realizar esta accion'},status = status.HTTP_400_BAD_REQUEST)  
        else:
            return Response(userSerializer.errors,status = status.HTTP_400_BAD_REQUEST) 

class userUpdateAPIView(Authentication,generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(estado = 1,id = self.userFull.id).first()

    def put(self,request):
        userUpdateSerializer = self.get_serializer(data = request.data)
        if userUpdateSerializer.is_valid(): 
            user = self.get_queryset()
            if user:
                userUpdate = self.serializer_class(user,data = userUpdateSerializer.validated_data)
                if userUpdate.is_valid():
                    user.name = userUpdate.validated_data['name']
                    user.last_name = userUpdate.validated_data['last_name']
                    if userUpdate.validated_data['password'] != None and userUpdate.validated_data['password'] != "":
                        user.set_password(userUpdate.validated_data['password'])
                        #context = {'email':data['email'],'domain':data['domain'],'usuario':data['usuario'],'password':data['password']}
                        data = {'email':user.correo,'domain':'https://fipdigital.info','usuario':user,'password':userUpdate.validated_data['password']}
                        send_password(data)
                    if userUpdate.validated_data['avatar'] != None and userUpdate.validated_data['avatar'] != "":
                        user.avatar = userUpdate.validated_data['avatar']
                    folderMasterPrivate = Folder.objects.get(scope = False,
                                                        unidadArea_id = self.userFull.unidadArea_id,
                                                        user_id =self.userFull.id,
                                                        carpeta_hija__isnull =True,eliminado = False)
                    folderMasterPrivate.nombre = "Carpeta privada de "+ userUpdate.validated_data['name'][:1].upper() + userUpdate.validated_data['name'][1:] + " " + userUpdate.validated_data['last_name'][:1].upper() + "."
                    folderMasterPrivate.save()
                    user.save()
                    return Response({'Mensaje':'Usuario actualizado correctamente'},status = status.HTTP_200_OK)
                return Response(userUpdate.errors,status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'Error':'No se puede validar el usario'},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(userUpdateSerializer.errors,status = status.HTTP_400_BAD_REQUEST)