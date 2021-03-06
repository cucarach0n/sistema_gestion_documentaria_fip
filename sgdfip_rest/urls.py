"""sgdfip_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
#yasg
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings

schema_view = get_schema_view(
   openapi.Info(
      title="Sistema Gestion Documentaria API",
      default_version='v0.8.0',
      description="Sistema para el almacenamiento masivo de archivos",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="devalo19@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('usuario/', include('apps.users.api.urls')),
    #path('sgdapi/', include('apps.sgdapi.api.routers')),
    path('file/', include('apps.file.api.routers')),
    path('folder/', include('apps.folder.api.routers')),
    path('tag/', include('apps.tag.api.routers')),
    path('unidadArea/', include('apps.unidadArea.api.routers')),
    path('etiqueta/', include('apps.etiqueta.api.routers')),
    path('share/', include('apps.share.api.routers')),
    path('caracteristica/', include('apps.caracteristica.api.routers')),
    path('utils/', include('apps.adminutils.api.routers')),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)