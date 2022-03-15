from apps.share.api.views.folderShare_views import FolderShareViewSet
from apps.share.api.views.fileShare_views import FileShareViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'folder',FolderShareViewSet, basename =  'FolderShare-view')
router.register(r'file',FileShareViewSet, basename =  'FileShare-view')
urlpatterns = router.urls