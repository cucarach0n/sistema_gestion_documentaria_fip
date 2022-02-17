from rest_framework.routers import DefaultRouter
from apps.tag.api.views.tag_views import TagAPIView,TagListAPIView,TagBuscarAPIView
router = DefaultRouter()

router.register(r'ver',TagListAPIView, basename = 'TagList-view')
router.register(r'crear',TagAPIView, basename =  'Tag-view')
router.register(r'find',TagBuscarAPIView, basename =  'TagBuscar-view')
urlpatterns = router.urls