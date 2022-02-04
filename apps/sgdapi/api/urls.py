from distutils.command.build_scripts import first_line_re
from django.urls import path
from apps.sgdapi.api.api import *
from apps.sgdapi.api.views.general_views import DocumentoListAPIView
from apps.sgdapi.api.views.documento_views import DocumentoCreateAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('usuario/',usuario_api_view,name = 'usuario_api'),
    path('usuario/<int:pk>/',usuario_detail_api_view,name = 'usuario-detail'),
    path('documento/list/',DocumentoListAPIView.as_view(),name = 'documento_list'),
    path('documento/create/',DocumentoCreateAPIView.as_view(),name = 'documento_create'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)