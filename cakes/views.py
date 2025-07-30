from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from rest_framework import viewsets
from .models import Cake, CartItem, Order, OrderItem
from .serializers import CakeSerializer, OrderSerializer
from .models import Store
from .serializers import StoreSerializer, CartItemSerializer
from rest_framework.permissions import IsAdminUser
from django.db.models import Sum, Count
from rest_framework.decorators import api_view, permission_classes
from django.db import models


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        token = Token.objects.create(user=user)
        return Response({'token': token.key})


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'})


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })
    
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'message': 'Account deleted successfully'}, status=204)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not user.check_password(current_password):
            return Response({"error": "Incorrect current password"}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"})

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        username = request.data.get("username")
        email = request.data.get("email")

        if username:
            user.username = username
        if email:
            user.email = email

        user.save()
        return Response({"message": "Profile updated successfully"})


class CakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer
    permission_classes = [IsAuthenticated]

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer



class CartListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        cake_id = data.get("cake")
        quantity = data.get("quantity", 1)
        customization = data.get("customization", "")

        try:
            cake = Cake.objects.get(id=cake_id)
        except Cake.DoesNotExist:
            return Response({"error": "Cake not found."}, status=404)

        cart_item, created = CartItem.objects.get_or_create(user=request.user, cake=cake)
        cart_item.quantity = quantity
        cart_item.customization = customization
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=201)


class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        try:
            item = CartItem.objects.get(id=id, user=request.user)
            item.delete()
            return Response(status=204)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found."}, status=404)


class UpdateCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id):
        try:
            item = CartItem.objects.get(id=id, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found."}, status=404)

        item.quantity = request.data.get("quantity", item.quantity)
        item.customization = request.data.get("customization", item.customization)
        item.save()
        return Response(CartItemSerializer(item).data)

# GET /api/analytics/sales/
@api_view(['GET'])
@permission_classes([IsAdminUser])
def sales_analytics(request):
    total_sales = CartItem.objects.aggregate(total=Sum('cake__price'))['total'] or 0
    total_orders = CartItem.objects.count()
    
    return Response({
        "total_sales": total_sales,
        "total_orders": total_orders
    })

# GET /api/analytics/top-cakes/
@api_view(['GET'])
@permission_classes([IsAdminUser])
def top_selling_cakes(request):
    top_cakes = (CartItem.objects
                 .values('cake__id', 'cake__name')
                 .annotate(sold=Count('id'))
                 .order_by('-sold')[:5])
    
    return Response(top_cakes)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    data = request.data  # expects: { "items": [{"cake": 1, "quantity": 2}, ...] }
    order = Order.objects.create(user=request.user)
    
    for item in data.get("items", []):
        try:
            cake = Cake.objects.get(id=item["cake"])
            quantity = item.get("quantity", 1)
            OrderItem.objects.create(order=order, cake=cake, quantity=quantity)
        except Cake.DoesNotExist:
            return Response({"error": f"Cake with id {item['cake']} not found."}, status=400)
    
    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, id):
    try:
        order = Order.objects.get(id=id, user=request.user)
        return Response(OrderSerializer(order).data)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # Base queryset (will be filtered below)
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return orders belonging to the logged-in user
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user when placing an order
        serializer.save(user=self.request.user)

    def get_object(self):
        # Ensure user can access only their own order
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You don't have access to this order.")
        return obj