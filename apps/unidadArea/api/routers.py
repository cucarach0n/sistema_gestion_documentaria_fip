from rest_framework.routers import DefaultRouter
from apps.unidadArea.api.views.unidadArea_views import unidadAreaListAPIView,unidadAreaCreateAPIView,unidadAreaBuscarAPIView,unidadAreaDeleteAPIView, unidadAreaUpdatePIView
router = DefaultRouter()

router.register(r'ver',unidadAreaListAPIView, basename = 'unidadAreaVer-view')
router.register(r'create',unidadAreaCreateAPIView, basename = 'unidadAreaCreate-view')
router.register(r'find',unidadAreaBuscarAPIView, basename = 'unidadAreaBuscar-view')
router.register(r'eliminar',unidadAreaDeleteAPIView, basename = 'unidadAreaBuscar-view')
router.register(r'update',unidadAreaUpdatePIView, basename = 'unidadAreaUpdate-view')
urlpatterns = router.urls