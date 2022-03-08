from rest_framework.routers import DefaultRouter
from apps.folder.api.views.folder_in_folder_views import FolderInFolderViewSet
from apps.folder.api.views.folder_views import FolderViewSet,FolderDeleteAPIView,FolderUpdateAPIView,FolderHistoryAPIView
router = DefaultRouter()

router.register(r'parent',FolderViewSet, basename =  'Folder-view')
router.register(r'child',FolderInFolderViewSet, basename =  'Subdirectorio-view')
router.register(r'eliminar',FolderDeleteAPIView, basename =  'eliminarFolder-view')
router.register(r'update',FolderUpdateAPIView, basename =  'updateFolder-view')
router.register(r'history',FolderHistoryAPIView, basename =  'historyFolder-view')
urlpatterns = router.urls