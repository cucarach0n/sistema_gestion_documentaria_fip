from rest_framework.routers import DefaultRouter
from apps.file.api.views.file_views import FileViewSet,FileObtenerViewSet,FileBuscarAPIView,FileListViewSet, FileHistoryAPIView
from apps.file.api.views.fileTag_views import FileTagAPIView,FileTagDeleteAPIView
from apps.file.api.views.general_views import FileListAPIView
router = DefaultRouter()

router.register(r'upload',FileViewSet, basename = 'upload-view')
router.register(r'all',FileListAPIView, basename =  'all-view')
router.register(r'tag',FileTagAPIView, basename =  'FileTagList-view')
router.register(r'ver',FileObtenerViewSet, basename =  'FileGet-view')
router.register(r'eliminar',FileTagDeleteAPIView, basename =  'FileTagDelete-view')
router.register(r'find',FileBuscarAPIView, basename =  'FileBuscar-view')
router.register(r'obtener',FileListViewSet, basename =  'FileObtener-view')
router.register(r'history',FileHistoryAPIView, basename =  'historyFile-view')
urlpatterns = router.urls