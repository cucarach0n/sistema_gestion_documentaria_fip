from rest_framework.routers import DefaultRouter
from apps.sgdapi.api.views.documento_views import DocumentoViewSet
from apps.sgdapi.api.views.general_views import DocumentoListAPIView
router = DefaultRouter()

router.register(r'documento',DocumentoViewSet, basename = 'Documento-view')
router.register(r'documentos',DocumentoListAPIView, basename =  'Documentos-view')
urlpatterns = router.urls