from apps.share.api.views.folderShare_views import FolderShareViewSet, FolderShareCloneViewSet
from apps.share.api.views.fileShare_views import FileShareViewSet,FileShareCloneViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'folder',FolderShareViewSet, basename =  'FolderShare-view')
router.register(r'file',FileShareViewSet, basename =  'FileShare-view')
router.register(r'folderClone',FolderShareCloneViewSet, basename =  'FolderCloneShare-view')
router.register(r'fileClone',FileShareCloneViewSet, basename =  'FileCloneShare-view')
urlpatterns = router.urls