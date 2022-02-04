from django.urls import path
from apps.users.api.api import UserAPIView,UserCreateAPIView,userActivateRetrieveAPIView

urlpatterns = [
    path('list/',UserAPIView.as_view(),name = 'usuario-api'),
    path('create/',UserCreateAPIView.as_view(),name = 'usuario-create'),
    path('validar/<str:token>',userActivateRetrieveAPIView.as_view(),name = 'usuario-activar')
]