from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from products.serializers import ProductListSerializer

class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items"""
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value

class CartSerializer(serializers.ModelSerializer):
    """Serializer for shopping cart"""
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'total_items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items"""
    product = ProductListSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total_price', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders"""
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user_email', 'status', 'total_price', 'total_items',
            'shipping_address', 'phone_number', 'notes', 'items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user_email', 'total_price', 'created_at', 'updated_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders"""
    
    class Meta:
        model = Order
        fields = ['shipping_address', 'phone_number', 'notes']
    
    def validate_shipping_address(self, value):
        if not value.strip():
            raise serializers.ValidationError("Shipping address is required")
        return value
    
    def validate_phone_number(self, value):
        if not value.strip():
            raise serializers.ValidationError("Phone number is required")
        return value
