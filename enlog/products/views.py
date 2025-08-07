from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.cache import cache
from django.conf import settings
from .models import Category, Product
from .serializers import (
    CategorySerializer, ProductSerializer, ProductListSerializer, 
    ProductCreateUpdateSerializer
)

class CategoryListCreateView(generics.ListCreateAPIView):
    """List all categories or create a new category"""
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def get_queryset(self):
        # Try to get from cache first
        cache_key = 'categories_list'
        cached_categories = cache.get(cache_key)
        
        if cached_categories is None:
            queryset = Category.objects.filter(is_active=True).prefetch_related('products')
            cache.set(cache_key, list(queryset), settings.CACHE_TTL)
            return queryset
        
        return Category.objects.filter(id__in=[cat.id for cat in cached_categories])

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a category"""
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
    
    def get_queryset(self):
        return Category.objects.all()

class ProductListCreateView(generics.ListCreateAPIView):
    """List all products with filtering and caching or create a new product"""
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductListSerializer
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        # Manual filtering
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        price_min = self.request.query_params.get('price_min')
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        
        price_max = self.request.query_params.get('price_max')
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        
        in_stock = self.request.query_params.get('in_stock')
        if in_stock is not None:
            if in_stock.lower() == 'true':
                queryset = queryset.filter(stock__gt=0)
            elif in_stock.lower() == 'false':
                queryset = queryset.filter(stock=0)
        
        featured = self.request.query_params.get('featured')
        if featured is not None:
            queryset = queryset.filter(featured=featured.lower() == 'true')
        
        return queryset

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a product"""
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductSerializer
    
    def get_queryset(self):
        return Product.objects.select_related('category')
    
    def retrieve(self, request, *args, **kwargs):
        # Try to get from cache first
        product_id = kwargs.get('pk')
        cache_key = f'product_{product_id}'
        cached_product = cache.get(cache_key)
        
        if cached_product is None:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            cache.set(cache_key, serializer.data, settings.CACHE_TTL)
            return Response(serializer.data)
        
        return Response(cached_product)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_products(request):
    """Get featured products"""
    cache_key = 'featured_products'
    cached_products = cache.get(cache_key)
    
    if cached_products is None:
        products = Product.objects.filter(is_active=True, featured=True).select_related('category')[:8]
        serializer = ProductListSerializer(products, many=True)
        cache.set(cache_key, serializer.data, settings.CACHE_TTL)
        return Response(serializer.data)
    
    return Response(cached_products)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def products_by_category(request, category_id):
    """Get products by category"""
    cache_key = f'category_{category_id}_products'
    cached_products = cache.get(cache_key)
    
    if cached_products is None:
        products = Product.objects.filter(
            category_id=category_id, 
            is_active=True
        ).select_related('category')
        serializer = ProductListSerializer(products, many=True)
        cache.set(cache_key, serializer.data, settings.CACHE_TTL)
        return Response(serializer.data)
    
    return Response(cached_products)
