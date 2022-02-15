from rest_framework.routers import DefaultRouter
from apps.tag.api.views.tag_views import TagAPIView,TagListAPIView
router = DefaultRouter()

router.register(r'ver',TagListAPIView, basename = 'TagList-view')
router.register(r'crear',TagAPIView, basename =  'Tag-view')
urlpatterns = router.urls