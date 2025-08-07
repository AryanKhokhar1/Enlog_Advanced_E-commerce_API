from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class CartItemInline(admin.TabularInline):
    """Inline admin for cart items"""
    model = CartItem
    extra = 0
    readonly_fields = ('total_price',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin configuration for Cart model"""
    list_display = ('user', 'total_items', 'total_price', 'created_at', 'updated_at')
    search_fields = ('user__email', 'user__username')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('total_items', 'total_price', 'created_at', 'updated_at')
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    """Inline admin for order items"""
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price', 'created_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model"""
    list_display = ('id', 'user', 'status', 'total_price', 'total_items', 'created_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__email', 'user__username', 'shipping_address')
    list_editable = ('status',)
    readonly_fields = ('total_items', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'status', 'total_price')
        }),
        ('Shipping Details', {
            'fields': ('shipping_address', 'phone_number', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Send notification when order status is updated"""
        if change and 'status' in form.changed_data:
            # Import here to avoid circular imports
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'user_{obj.user.id}',
                {
                    'type': 'order_status_update',
                    'order_id': obj.id,
                    'old_status': Order.objects.get(id=obj.id).status,
                    'new_status': obj.status,
                    'message': f'Order #{obj.id} status updated to {obj.get_status_display()}'
                }
            )
        
        super().save_model(request, obj, form, change)
