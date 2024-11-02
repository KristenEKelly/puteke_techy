from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubtitleViewSet
from django.contrib import admin

router = DefaultRouter()
router.register(r'subtitles', SubtitleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include('search.urls')),
]
