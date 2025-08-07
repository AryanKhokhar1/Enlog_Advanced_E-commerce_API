import django_filters
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    """Filter class for Product model"""
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_stock')
    featured = django_filters.BooleanFilter()
    
    class Meta:
        model = Product
        fields = ['category', 'featured']
    
    def filter_stock(self, queryset, name, value):
        if value is True:
            return queryset.filter(stock__gt=0)
        elif value is False:
            return queryset.filter(stock=0)
        return queryset
