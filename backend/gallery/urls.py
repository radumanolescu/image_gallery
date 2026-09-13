from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gallery.views import ImageMetadataViewSet

router = DefaultRouter()
router.register(r'images', ImageMetadataViewSet, basename='imagemetadata')

urlpatterns = [
    path('api/', include(router.urls)),
]