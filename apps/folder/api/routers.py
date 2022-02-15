from rest_framework.routers import DefaultRouter
from apps.folder.api.views.folder_in_folder_views import FolderInFolderViewSet
from apps.folder.api.views.folder_views import FolderViewSet
router = DefaultRouter()

router.register(r'parent',FolderViewSet, basename =  'Folder-view')
router.register(r'child',FolderInFolderViewSet, basename =  'Subdirectorio-view')
urlpatterns = router.urls