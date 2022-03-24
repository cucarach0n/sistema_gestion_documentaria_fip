from rest_framework.routers import DefaultRouter
from apps.folder.api.views.folder_in_folder_views import FolderInFolderViewSet,FolderInFolderPrivateViewSet
from apps.folder.api.views.folder_views import FolderViewSet,FolderDeleteAPIView,FolderUpdateAPIView,FolderHistoryAPIView,FolderBuscarAPIView,FolderPrivateViewSet,FolderUpdatePrivateAPIView
router = DefaultRouter()

router.register(r'parent',FolderViewSet, basename =  'Folder-view')
#router.register(r'parentPrivate',FolderPrivateViewSet, basename =  'FolderPrivate-view')
router.register(r'child',FolderInFolderViewSet, basename =  'Subdirectorio-view')
#router.register(r'childPrivate',FolderInFolderPrivateViewSet, basename =  'SubdirectorioPrivate-view')
router.register(r'eliminar',FolderDeleteAPIView, basename =  'eliminarFolder-view')
router.register(r'update',FolderUpdateAPIView, basename =  'updateFolder-view')
router.register(r'updatePrivate',FolderUpdatePrivateAPIView, basename =  'updatePrivateFolder-view')
router.register(r'history',FolderHistoryAPIView, basename =  'historyFolder-view')
router.register(r'buscar',FolderBuscarAPIView, basename =  'findFolder-view')
urlpatterns = router.urls