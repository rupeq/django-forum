from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, UserStatisticViewSet


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'statistic', UserStatisticViewSet)

urlpatterns = router.urls
