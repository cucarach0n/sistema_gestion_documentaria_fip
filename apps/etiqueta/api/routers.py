from rest_framework.routers import DefaultRouter
from apps.etiqueta.api.views.etiqueta_views import EtiquetaCreateViewSet,EtiquetaBuscarViewSet
router = DefaultRouter()

router.register(r'crud',EtiquetaCreateViewSet, basename =  'Etiqueta-view')
router.register(r'find',EtiquetaBuscarViewSet, basename =  'Etiqueta-view')
#router.register(r'eliminar',EtiquedaEliminarViewSet, basename =  'Etiqueta-view')
urlpatterns = router.urls