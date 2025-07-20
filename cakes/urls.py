from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CakeViewSet, RegisterView, LoginView, LogoutView, UserView
from django.http import HttpResponse

router = DefaultRouter()
router.register(r'cakes', CakeViewSet)

def index(request):
    return HttpResponse("Welcome to DelightAPI")

urlpatterns = [
    path('', index, name='home'),  # homepage view
    path('', include(router.urls)),  # DRF router endpoints like /cakes/
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/user/', UserView.as_view(), name='user'),
]

