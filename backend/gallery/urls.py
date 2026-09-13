from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gallery.views import ImageMetadataViewSet
from gallery.auth_views import CsrfView, LoginView, LogoutView, MeView

router = DefaultRouter()
router.register(r'images', ImageMetadataViewSet, basename='imagemetadata')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/csrf/', CsrfView.as_view(), name='csrf'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/me/', MeView.as_view(), name='me'),
]