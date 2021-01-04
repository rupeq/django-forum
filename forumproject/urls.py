from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from rest_framework import routers

from app.views import UserView

router = routers.DefaultRouter()
router.register(r'user', UserView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('app.urls')),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
