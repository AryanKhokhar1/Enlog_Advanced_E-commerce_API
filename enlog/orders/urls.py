from django.urls import path
from . import views

urlpatterns = [
    # Cart URLs
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/items/', views.CartItemView.as_view(), name='cart-item-add'),
    path('cart/items/<int:item_id>/', views.CartItemView.as_view(), name='cart-item-detail'),
    
    # Order URLs
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:order_id>/status/', views.OrderStatusUpdateView.as_view(), name='order-status-update'),
]
