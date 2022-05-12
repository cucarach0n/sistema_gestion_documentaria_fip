from apps.caracteristica.api.views.caracteristicaFile_views import CaracteristicaFileDeleteViewSet, CaracteristicaFileViewSet
from apps.caracteristica.api.views.caracteristica_views import CaracteristicaViewSet
from apps.caracteristica.api.views.tipoCaracteristica_views import tipoCaracteristicaViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'crear',CaracteristicaViewSet, basename =  'caracteristica-view')
router.register(r'tipo',tipoCaracteristicaViewSet, basename =  'tipoCaracteristica-view')
router.register(r'file',CaracteristicaFileViewSet, basename =  'fileCaracteristica-view')
router.register(r'eliminarFile',CaracteristicaFileDeleteViewSet, basename =  'fileCaracteristica-view')
urlpatterns = router.urls