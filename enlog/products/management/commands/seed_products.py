from django.core.management.base import BaseCommand
from products.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seed the database with sample products and categories'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample categories and products...')
        
        # Create categories
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Electronic devices and gadgets',
                'image': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=500'
            },
            {
                'name': 'Clothing',
                'description': 'Fashion and apparel',
                'image': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=500'
            },
            {
                'name': 'Books',
                'description': 'Books and educational materials',
                'image': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=500'
            },
            {
                'name': 'Home & Garden',
                'description': 'Home improvement and garden supplies',
                'image': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500'
            },
            {
                'name': 'Sports',
                'description': 'Sports equipment and accessories',
                'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500'
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create products
        products_data = [
            # Electronics
            {
                'name': 'Smartphone Pro Max',
                'description': 'Latest flagship smartphone with advanced features',
                'price': Decimal('999.99'),
                'stock': 50,
                'category': 'Electronics',
                'sku': 'PHONE001',
                'featured': True,
                'image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500'
            },
            {
                'name': 'Wireless Headphones',
                'description': 'High-quality wireless headphones with noise cancellation',
                'price': Decimal('299.99'),
                'stock': 75,
                'category': 'Electronics',
                'sku': 'HEAD001',
                'featured': True,
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500'
            },
            {
                'name': 'Laptop Ultra',
                'description': 'Powerful laptop for work and gaming',
                'price': Decimal('1599.99'),
                'stock': 25,
                'category': 'Electronics',
                'sku': 'LAP001',
                'featured': True,
                'image': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500'
            },
            
            # Clothing
            {
                'name': 'Classic T-Shirt',
                'description': 'Comfortable cotton t-shirt in various colors',
                'price': Decimal('29.99'),
                'stock': 100,
                'category': 'Clothing',
                'sku': 'TSHIRT001',
                'featured': False,
                'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500'
            },
            {
                'name': 'Designer Jeans',
                'description': 'Premium denim jeans with perfect fit',
                'price': Decimal('89.99'),
                'stock': 60,
                'category': 'Clothing',
                'sku': 'JEANS001',
                'featured': True,
                'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=500'
            },
            
            # Books
            {
                'name': 'Python Programming Guide',
                'description': 'Comprehensive guide to Python programming',
                'price': Decimal('49.99'),
                'stock': 40,
                'category': 'Books',
                'sku': 'BOOK001',
                'featured': False,
                'image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500'
            },
            {
                'name': 'Web Development Handbook',
                'description': 'Complete handbook for modern web development',
                'price': Decimal('39.99'),
                'stock': 35,
                'category': 'Books',
                'sku': 'BOOK002',
                'featured': False,
                'image': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=500'
            },
            
            # Home & Garden
            {
                'name': 'Smart Home Hub',
                'description': 'Central hub for all your smart home devices',
                'price': Decimal('199.99'),
                'stock': 30,
                'category': 'Home & Garden',
                'sku': 'HOME001',
                'featured': True,
                'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500'
            },
            {
                'name': 'Garden Tool Set',
                'description': 'Complete set of essential garden tools',
                'price': Decimal('79.99'),
                'stock': 45,
                'category': 'Home & Garden',
                'sku': 'GARDEN001',
                'featured': False,
                'image': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=500'
            },
            
            # Sports
            {
                'name': 'Professional Tennis Racket',
                'description': 'High-performance tennis racket used by professionals',
                'price': Decimal('249.99'),
                'stock': 20,
                'category': 'Sports',
                'sku': 'TENNIS001',
                'featured': False,
                'image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=500'
            },
            {
                'name': 'Fitness Tracker Watch',
                'description': 'Advanced fitness tracker with heart rate monitoring',
                'price': Decimal('199.99'),
                'stock': 55,
                'category': 'Sports',
                'sku': 'FITNESS001',
                'featured': True,
                'image': 'https://images.unsplash.com/photo-1544117519-31a4b719223d?w=500'
            }
        ]
        
        for product_data in products_data:
            category_name = product_data.pop('category')
            product_data['category'] = categories[category_name]
            
            product, created = Product.objects.get_or_create(
                sku=product_data['sku'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(categories_data)} categories and {len(products_data)} products'
            )
        )
