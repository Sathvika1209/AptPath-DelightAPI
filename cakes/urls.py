from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CakeViewSet

router = DefaultRouter()
router.register(r'cakes', CakeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
