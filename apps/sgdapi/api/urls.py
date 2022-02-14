from distutils.command.build_scripts import first_line_re
from django.urls import path
from apps.sgdapi.api.api import *
from apps.sgdapi.api.views.documento_views import FileCreateAPIView

from django.conf.urls.static import static

urlpatterns = [
    #path('usuario/',usuario_api_view,name = 'usuario_api'),
    #path('usuario/<int:pk>/',usuario_detail_api_view,name = 'usuario-detail'),
    #path('documento/list/',DocumentoListAPIView.as_view(),name = 'documento_list'),
    path('file/',FileCreateAPIView.as_view(),name = 'file_list')
]
