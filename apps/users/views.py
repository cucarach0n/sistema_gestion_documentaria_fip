from django.contrib.sessions.models import Session
from datetime import datetime
from apps.base.util import setHistory
from apps.folder.models import Folder
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from apps.users.authenticacion_mixings import Authentication
from apps.users.api.serializers.user_serializers import UserTokenSerializer
from django.contrib.auth import authenticate

class UserToken(Authentication,APIView):
    
    def post(self,request,*args,**kwargs):
        
        #print(self.user)
        #username = request.GET.get('username')
        #print(username)
        #testTemplate()
        try:
            folder = Folder.objects.filter(carpeta_hija__isnull =True,unidadArea_id = self.userFull.unidadArea_id).first()
            #print(folder)
            user_token,create = Token.objects.get_or_create(user = self.user)
            #print(user_token.created)
            user = UserTokenSerializer(self.user)
            #set history user
            #setHistory(user,"Solicitud token nuevo",user.id)
            return Response({
                'token': user_token.key,
                'user' : user.data,
                'slugPadre': folder.slug,
                'carpetaPadre': folder.nombre
                },status = status.HTTP_200_OK)
            
        except:
            return Response({
                'error': 'Credenciales enviadas incorrectas'
                },status = status.HTTP_400_BAD_REQUEST)

class Login(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        login_serializer = self.serializer_class(data = request.data,context = {'request':request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                user = authenticate(username=request.data['username'],password=request.data['password'])
                '''if user is not None:
                    print('"Usuario autenticado')'''
                print('usuario autenticado')
                token,created = Token.objects.get_or_create(user = user)
                user_serializer = UserTokenSerializer(user)
                #user_serializer.data['avatar'] = 'asdasd'
                #print(user.avatar)
                
                user.last_login = datetime.today()
                user.save()
                #set history user
                setHistory(user,"inicio de sesion",user.id)
                if created:
                    return Response({
                        'token':token.key,
                        'user':user_serializer.data,
                        'mensaje':'Inicio de sesion exitoso'
                    },status = status.HTTP_201_CREATED)
                else:
                    
                    all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({
                        'token':token.key,
                        'user':user_serializer.data,
                        'mensaje':'Inicio de sesion exitoso'
                    },status = status.HTTP_201_CREATED) 
                    
                    #return Response({'error':'Ya se ha iniciado sesion con este usuario'},status = status.HTTP_409_CONFLICT)
                return Response({'error':'error en validar avatar'},status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':'Este usuario no puede iniciar sesion, deve activar su cuenta primero'},status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error':'Datos del usuario invalidos'},status = status.HTTP_400_BAD_REQUEST)
        #return Response({'mensaje':'Hola desde response'}, status = status.HTTP_200_OK)


class Logout(Authentication,APIView):
    '''
    def get(self,request,*args,**kwargs):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key = token).first()
            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()            
                session_message = 'Sesiones de usuario eliminadas.'
                token_message = 'Token Eliminado'
                return Response({'token_message':token_message,'session_message':session_message},status = status.HTTP_200_OK)   
            else:
                return Response({'error':'No se ha encontrado un usuario con estas credenciales'},status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error':'No se ha encontrado token en la peticion'},status = status.HTTP_409_CONFLICT)
    '''

        
    def post(self,request):
        print(self.user)
        #username = request.GET.get('username')
        #print(username)
        try:
            user_token,create = Token.objects.get_or_create(user = self.user)
            user = UserTokenSerializer(self.user)
            if user_token:
                user = user_token.user
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                user_token.delete()            
                session_message = 'Sesiones de usuario eliminadas.'
                token_message = 'Token Eliminado'
                return Response({'token_message':token_message,'session_message':session_message},status = status.HTTP_200_OK)   
            else:
                return Response({'error':'No se ha encontrado un usuario con estas credenciales'},status = status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error':'Usuario no logeado'},status = status.HTTP_409_CONFLICT)
