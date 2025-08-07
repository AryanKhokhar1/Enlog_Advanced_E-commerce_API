from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Cart, CartItem, Order, OrderItem
from .serializers import (
    CartSerializer, CartItemSerializer, OrderSerializer, OrderCreateSerializer
)
from products.models import Product

class CartView(APIView):
    #Shopping cart view
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        #Get user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def delete(self, request):
        """Clear cart"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared successfully'})

class CartItemView(APIView):
    #Cart item management view
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        #Add item to cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if product.stock < quantity:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, item_id):
        #Update cart item quantity
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        quantity = request.data.get('quantity')
        if not quantity or quantity <= 0:
            return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)
        
        if cart_item.product.stock < quantity:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)
    
    def delete(self, request, item_id):
        #Remove item from cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        return Response({'message': 'Item removed from cart'})

class OrderListCreateView(generics.ListCreateAPIView):
    #List orders and create new order
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('items__product')
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        #Create order from cart
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate stock availability
        for cart_item in cart.items.all():
            if cart_item.product.stock < cart_item.quantity:
                return Response(
                    {'error': f'Insufficient stock for {cart_item.product.name}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Create order
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order = serializer.save(
            user=request.user,
            total_price=cart.total_price
        )
        
        # Create order items and update stock
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            # Reduce stock
            cart_item.product.reduce_stock(cart_item.quantity)
        
        # Clear cart
        cart.items.all().delete()
        
        # Send notification via WebSocket
        self.send_order_notification(order.user.id, order.id, 'Order created successfully')
        
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    
    def send_order_notification(self, user_id, order_id, message):
        #Send order notification via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_{user_id}',
            {
                'type': 'order_notification',
                'order_id': order_id,
                'message': message
            }
        )

class OrderDetailView(generics.RetrieveAPIView):
    #Order detail view
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('items__product')

class OrderStatusUpdateView(APIView):
    #Update order status (Admin only)
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def patch(self, request, order_id):
        #Update order status
        order = get_object_or_404(Order, id=order_id)
        new_status = request.data.get('status')
        
        if new_status not in [choice[0] for choice in Order.STATUS_CHOICES]:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        old_status = order.status
        order.status = new_status
        order.save()
        
        # Send notification via WebSocket
        self.send_status_notification(order.user.id, order.id, old_status, new_status)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def send_status_notification(self, user_id, order_id, old_status, new_status):
        #Send status update notification via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_{user_id}',
            {
                'type': 'order_status_update',
                'order_id': order_id,
                'old_status': old_status,
                'new_status': new_status,
                'message': f'Order #{order_id} status updated from {old_status} to {new_status}'
            }
        )
