from rest_framework.routers import DefaultRouter
from apps.etiqueta.api.views.etiqueta_views import EtiquetaViewSet
router = DefaultRouter()

router.register(r'create',EtiquetaViewSet, basename =  'Etiqueta-view')
urlpatterns = router.urls