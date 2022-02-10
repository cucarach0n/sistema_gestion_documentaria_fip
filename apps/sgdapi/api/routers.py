from rest_framework.routers import DefaultRouter
from apps.sgdapi.api.views.documento_views import DocumentoViewSet,DocumentoObtenerViewSet
from apps.sgdapi.api.views.general_views import DocumentoListAPIView
router = DefaultRouter()

router.register(r'documento',DocumentoViewSet, basename = 'Documento-view')
router.register(r'documentos',DocumentoListAPIView, basename =  'Documentos-view')
router.register(r'ver',DocumentoObtenerViewSet, basename =  'DocumentoObtener-view')

urlpatterns = router.urls