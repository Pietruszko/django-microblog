"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import RegisterView
from django.conf import settings
from django.conf.urls.static import static
from posts.views import PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested.routers import NestedDefaultRouter
from notifications.views import NotificationViewSet
from users.views import UserProfileViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

posts_router = NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

notifications_router = DefaultRouter()
notifications_router.register(r'notifications', NotificationViewSet, basename='notifications')

users_router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/', include(posts_router.urls)),
    path('api/', include(notifications_router.urls)),
    path('api/', include(users_router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)