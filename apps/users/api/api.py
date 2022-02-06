from multiprocessing import context
from apps.sgdapi.models import Contrasena_reinicio
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.models import User
from apps.users.api.serializers import UserSerializer,UserCreateSerializer
from rest_framework import status
from rest_framework import generics
from apps.sgdapi.api.serializers.general_serializers import Contrasena_reinicioSerializer
from apps.sgdapi.util import send_email
from datetime import datetime
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class UserAPIView(APIView):
    def get(self,request):
        users = User.objects.all()
        users_serializer = UserSerializer(users,many = True)
        return Response(users_serializer.data, status = status.HTTP_200_OK );
class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    def post(self,request):
        serializer = self.serializer_class(data = request.data,context = request.data)
        if serializer.is_valid():
            current_site = get_current_site(request).domain
            fs = FileSystemStorage(location='sgdfip_rest/media/avatars/')
            file = fs.save(request.FILES['avatar'].name,request.FILES['avatar'])
            fileurl = fs.url(file)
            print(fileurl)
            doc = fileurl[6:]
            absURl = 'http://'+current_site+'/media/avatars'+ doc
            serializer.validated_data['avatar'] = absURl
            user = serializer.save()

            datos = {'correo':user.correo,
                    'token':get_random_string(length=40),
                    'fechaCambio':datetime.today().strftime('%Y-%m-%d'),
                    'estado':1}
            contrasena_reinicioO = Contrasena_reinicioSerializer(data = datos)
            if contrasena_reinicioO.is_valid():
                userSendEmail = contrasena_reinicioO.save()
                
                absurl = 'http://'+current_site+'/usuario/validar/'+userSendEmail.token
                send_email({'email':'devalo19@gmail.com','domain': str(absurl)})

            return Response({'Mensaje':'Se registro el usuario correctamente'},status = status.HTTP_200_OK)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class userActivateRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = Contrasena_reinicioSerializer
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
                user.save();
                return Response({'Mensaje':'Usuario validado correctamente'},status = status.HTTP_200_OK)
                
            else:
                return Response({'Error':'No se pudo validar dicha informacion'},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Error':'No se pudo validar dicha informacion'},status = status.HTTP_400_BAD_REQUEST)




