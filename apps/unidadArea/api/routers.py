from rest_framework.routers import DefaultRouter
from apps.unidadArea.api.views.unidadArea_views import unidadAreaListAPIView,unidadAreaCreateAPIView,unidadAreaBuscarAPIView
router = DefaultRouter()

router.register(r'ver',unidadAreaListAPIView, basename = 'unidadAreaVer-view')
router.register(r'create',unidadAreaCreateAPIView, basename = 'unidadAreaCreate-view')
router.register(r'find',unidadAreaBuscarAPIView, basename = 'unidadAreaBuscar-view')
urlpatterns = router.urls