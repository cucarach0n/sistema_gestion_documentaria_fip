from distutils.command.build_scripts import first_line_re
from django.urls import path
from apps.sgdapi.api.api import *
from apps.sgdapi.api.views.general_views import DocumentoListAPIView
from apps.sgdapi.api.views.documento_views import DocumentoCreateAPIView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,re_path
from django.views.static import serve

re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})

urlpatterns = [
    path('usuario/',usuario_api_view,name = 'usuario_api'),
    path('usuario/<int:pk>/',usuario_detail_api_view,name = 'usuario-detail'),
    #path('documento/list/',DocumentoListAPIView.as_view(),name = 'documento_list'),
    path('documento/',DocumentoCreateAPIView.as_view(),name = 'documento_list'),
]
