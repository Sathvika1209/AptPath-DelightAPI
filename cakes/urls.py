from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CakeViewSet, StoreViewSet, RegisterView, LoginView, LogoutView, UserView, DeleteAccountView, ChangePasswordView, UpdateProfileView, CartListView, AddToCartView, RemoveFromCartView, UpdateCartView, sales_analytics, top_selling_cakes, place_order, list_orders, order_detail, OrderViewSet
from django.http import HttpResponse

router = DefaultRouter()
router.register(r'cakes', CakeViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'orders', OrderViewSet, basename='orders')

def index(request):
    return HttpResponse("Welcome to DelightAPI")

urlpatterns = [
    path('', index, name='home'),  # homepage view
    path('', include(router.urls)),  # DRF router endpoints like /cakes/
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/user/', UserView.as_view(), name='user'),
    path('auth/delete/', DeleteAccountView.as_view(), name='delete_account'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('auth/update/', UpdateProfileView.as_view(), name='update-profile'),
    path('cart/', CartListView.as_view()),
    path('cart/add/', AddToCartView.as_view()),
    path('cart/remove/<int:id>/', RemoveFromCartView.as_view()),
    path('cart/update/<int:id>/', UpdateCartView.as_view()),
    path('analytics/sales/', sales_analytics, name='sales_analytics'),
    path('analytics/top-cakes/', top_selling_cakes, name='top_selling_cakes'),
    path('orders/', place_order, name='place_order'),
    path('orders/', list_orders, name='list_orders'),
    path('orders/<int:id>/', order_detail, name='order_detail'),


]

