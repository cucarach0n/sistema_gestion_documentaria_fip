from rest_framework.routers import DefaultRouter
from apps.sgdapi.api.views.documento_views import FileViewSet,FileObtenerViewSet
from apps.sgdapi.api.views.general_views import FileListAPIView
router = DefaultRouter()

router.register(r'file',FileViewSet, basename = 'File-view')
router.register(r'files',FileListAPIView, basename =  'Files-view')
router.register(r'ver',FileObtenerViewSet, basename =  'FileObtener-view')
'''router.register(r'folder',FolderViewSet, basename =  'Folder-view')
router.register(r'subfolder',FolderInFolderViewSet, basename =  'Subdirectorio-view')'''
urlpatterns = router.urls