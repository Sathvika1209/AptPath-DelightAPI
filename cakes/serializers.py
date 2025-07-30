# serializers.py
from rest_framework import serializers
from .models import Cake, Store, CartItem, Order, OrderItem

class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    cake_name = serializers.ReadOnlyField(source='cake.name')

    class Meta:
        model = CartItem
        fields = ['id', 'cake', 'cake_name', 'quantity', 'customization', 'added_at']

class OrderItemSerializer(serializers.ModelSerializer):
    cake_name = serializers.CharField(source='cake.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'cake', 'cake_name', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'items']
        read_only_fields = ['user']