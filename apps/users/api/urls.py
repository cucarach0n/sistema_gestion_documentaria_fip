from django.urls import path
from apps.users.api.api import UserAPIView,UserCreateAPIView,userActivateRetrieveAPIView,verAvatar,userDeleteAPIView
from apps.users.views import Login,Logout,UserToken

urlpatterns = [
    path('login/',Login.as_view(),name = 'login'),
    path('logout/',Logout.as_view(),name = 'logout'),
    path('refresh-token/',UserToken.as_view(),name = 'refresh_token'),

    path('list/',UserAPIView.as_view(),name = 'usuario-api'),
    path('create/',UserCreateAPIView.as_view(),name = 'usuario-create'),
    path('validar/<str:token>/',userActivateRetrieveAPIView.as_view(),name = 'usuario-activar'),
    path('verAvatar/<str:avatar>/',verAvatar.as_view(),name = 'verAvatar-api'),
    path('eliminar/<int:pk>/',userDeleteAPIView.as_view(),name = 'eliminarAvatar-api')
]