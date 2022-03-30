from apps.file.api.views.file_trash_views import FileDeletePublicAPIView, FileRestaurarPublicAPIView
from rest_framework.routers import DefaultRouter
from apps.file.api.views.file_views import (FileViewSet,
                                            FileObtenerViewSet,
                                            FileBuscarAPIView,
                                            FileListViewSet,
                                            FileHistoryAPIView,
                                            FileUpdatePrivateViewSet,
                                            FileDeleteAPIView,
                                            FileRestaurarAPIView)
from apps.file.api.views.fileTag_views import FileTagAPIView,FileTagDeleteAPIView
from apps.file.api.views.general_views import FileListAPIView
router = DefaultRouter()

router.register(r'upload',FileViewSet, basename = 'upload-view')
router.register(r'updatePrivate',FileUpdatePrivateViewSet, basename = 'updatePrivateFile-view')
#router.register(r'uploadPrivate',FilePrivateViewSet, basename = 'uploadPrivate-view')
router.register(r'all',FileListAPIView, basename =  'all-view')
router.register(r'tag',FileTagAPIView, basename =  'FileTagList-view')
router.register(r'ver',FileObtenerViewSet, basename =  'FileGet-view')
router.register(r'eliminar',FileTagDeleteAPIView, basename =  'FileTagDelete-view')
router.register(r'find',FileBuscarAPIView, basename =  'FileBuscar-view')
router.register(r'obtener',FileListViewSet, basename =  'FileObtener-view')
router.register(r'history',FileHistoryAPIView, basename =  'historyFile-view')
router.register(r'eliminarFile',FileDeleteAPIView, basename =  'eliminarFile-view')
router.register(r'restaurarFile',FileRestaurarAPIView, basename =  'restaurarFile-view')
#trash publico
router.register(r'eliminarFilePublic',FileDeletePublicAPIView, basename =  'eliminarFilePublic-view')
router.register(r'restaurarFilePublic',FileRestaurarPublicAPIView, basename =  'restaurarFilePublic-view')
urlpatterns = router.urls