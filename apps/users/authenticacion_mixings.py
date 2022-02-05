#from email import message
#from json import tool
#from secrets import token_urlsafe
#from typing import type_check_only
from rest_framework.renderers import JSONRenderer
from xmlrpc.client import ResponseError
from rest_framework.authentication import get_authorization_header
from apps.users.authentication import ExpiringTokenAuthentication
from rest_framework.response import Response
from rest_framework import status

class Authentication(object):
    user = None
    user_token_expire = False
    def get_user(self,request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
                
            except:
                return None
            token_expire = ExpiringTokenAuthentication()
            
            user,token,message,self.user_token_expire = token_expire.authenticate_credentials(token)
            if user != None and token != None:
                self.user = user
                return user
            return message
            print(token)
            
        return None
    def dispatch(self,request,*args,**kwargs):
        user = self.get_user(request)
        #se encontro un token en la peticion
        if user is not None:
            if type(user) == str:
                response = Response({'error':user,'expired':self.user_token_expire},status = status.HTTP_400_BAD_REQUEST)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = 'application/json'
                response.renderer_context = {}
                return response
            if not self.user_token_expire:
                return super().dispatch(request,*args,**kwargs)
        response = Response({'error':'No se han enviado las credenciales','expire':self.user_token_expire},status = status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response