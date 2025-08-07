from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model"""
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'name': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model"""
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'featured', 'created_at')
    list_filter = ('category', 'is_active', 'featured', 'created_at')
    search_fields = ('name', 'description', 'sku')
    list_editable = ('price', 'stock', 'is_active', 'featured')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'sku')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock')
        }),
        ('Display Options', {
            'fields': ('image', 'is_active', 'featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
