from django.db import models
from django.core.validators import MinValueValidator
from django.core.cache import cache

class Category(models.Model):
    #Product category model
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Invalidate cache when category is updated
        cache.delete_many([
            'categories_list',
            f'category_{self.id}',
            'products_list'
        ])

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.URLField(blank=True)
    sku = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['price']),
            models.Index(fields=['stock']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def is_in_stock(self):
        return self.stock > 0
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Invalidate cache when product is updated
        cache.delete_many([
            'products_list',
            f'product_{self.id}',
            f'category_{self.category.id}_products'
        ])
    
    def reduce_stock(self, quantity):
        """Reduce stock by given quantity"""
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            return True
        return False
