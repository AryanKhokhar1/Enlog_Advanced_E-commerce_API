from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model"""
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_admin', 'date_joined')
    list_filter = ('is_staff', 'is_admin', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone', 'address', 'date_of_birth', 'is_admin')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'phone', 'address', 'date_of_birth', 'is_admin')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile model"""
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__email', 'user__username')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
