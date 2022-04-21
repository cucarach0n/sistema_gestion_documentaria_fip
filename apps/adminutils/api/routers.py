
from apps.adminutils.api.views.disk_views import DiskViewSet
from apps.adminutils.api.views.utils_views import ContadorViewSet, TotalEspacioFileViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'disk',DiskViewSet, basename =  'disk-view')
router.register(r'totales',ContadorViewSet, basename =  'contador-view')
router.register(r'totalFile',TotalEspacioFileViewSet, basename =  'totalFile-view')
urlpatterns = router.urls