from rest_framework.routers import DefaultRouter
from apps.file.api.views.file_views import FileViewSet,FileObtenerViewSet
from apps.file.api.views.general_views import FileListAPIView
router = DefaultRouter()

router.register(r'upload',FileViewSet, basename = 'upload-view')
router.register(r'all',FileListAPIView, basename =  'all-view')
router.register(r'ver',FileObtenerViewSet, basename =  'FileObtener-view')
urlpatterns = router.urls