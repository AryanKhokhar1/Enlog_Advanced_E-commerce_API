# Advanced E-commerce API

A comprehensive Django REST API for an e-commerce system with JWT authentication, caching, real-time notifications, and advanced features.

## Features

### User Management
- JWT-based authentication using `djangorestframework-simplejwt`
- User registration and login
- Extended user profile management
- Order history tracking

### Product Management
- Product and Category CRUD operations
- Advanced filtering by category, price range, and stock availability
- Search functionality across products
- Admin-only product management
- Image support for products and categories

### Order System
- Shopping cart functionality
- Order placement and management
- Order status tracking (Pending → Shipped → Delivered)
- Real-time order status notifications via WebSockets
- Stock management (automatic stock reduction on order)

### Performance & Optimization
- Redis caching for products and categories
- Cache invalidation on data updates
- Database query optimization with `select_related` and `prefetch_related`
- Pagination for all list endpoints (10 items per page)

### Real-time Features
- WebSocket notifications for order status updates
- Django Channels integration
- Redis as channel layer backend

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | Django + Django REST Framework |
| Authentication | JWT (djangorestframework-simplejwt) |
| Database | PostgreSQL |
| Caching | Redis |
| Real-time | Django Channels |
| Admin | Django Admin |

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis Server
- pip (Python package manager)

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Enlog-Assessment
```

### 2. Create Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### Option A: SQLite3 (Default - No setup required)
The project is configured to use SQLite3 by default, which requires no additional setup.

#### Option B: PostgreSQL (Recommended for Production)

1. **Install PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS (with Homebrew)
brew install postgresql

# Start PostgreSQL service
sudo systemctl start postgresql  # Linux
brew services start postgresql   # macOS
```

2. **Create Database:**
```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE enlog_db;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE enlog_db TO postgres;
ALTER USER postgres CREATEDB;
\q
```

3. **Update Database Configuration:**
In `enlog/settings.py`, uncomment the PostgreSQL configuration and comment out SQLite:
```python
# Uncomment this for PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'enlog_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Comment this out when using PostgreSQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
```

4. **Create .env file:**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 5. Redis Setup
1. Install Redis server
2. Start Redis:
```bash
redis-server
```

### 6. Django Setup
```bash
cd enlog
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 7. Run the Application

#### Start Django Development Server
```bash
python manage.py runserver
```

#### Start Daphne for WebSocket Support (in another terminal)
```bash
daphne -p 8001 enlog.asgi:application
```

## API Endpoints

### Authentication
- `POST /auth/api/register/` - User registration
- `POST /auth/api/token/` - Login (get tokens)
- `POST /auth/api/token/refresh/` - Refresh access token
- `GET /auth/api/profile/` - Get user profile
- `PUT /auth/api/profile/` - Update user profile
- `GET /auth/api/orders/` - Get user's order history

### Products
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category (Admin only)
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category (Admin only)
- `DELETE /api/categories/{id}/` - Delete category (Admin only)
- `GET /api/categories/{id}/products/` - Get products by category

- `GET /api/products/` - List products (with filtering & pagination)
- `POST /api/products/` - Create product (Admin only)
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product (Admin only)
- `DELETE /api/products/{id}/` - Delete product (Admin only)
- `GET /api/products/featured/` - Get featured products

### Orders & Cart
- `GET /api/cart/` - Get user's cart
- `DELETE /api/cart/` - Clear cart
- `POST /api/cart/items/` - Add item to cart
- `PUT /api/cart/items/{id}/` - Update cart item
- `DELETE /api/cart/items/{id}/` - Remove item from cart

- `GET /api/orders/` - List user's orders
- `POST /api/orders/` - Create order from cart
- `GET /api/orders/{id}/` - Get order details
- `PATCH /api/orders/{id}/status/` - Update order status (Admin only)

### Query Parameters for Products
- `category` - Filter by category ID
- `price_min` - Minimum price filter
- `price_max` - Maximum price filter
- `in_stock` - Filter by stock availability (true/false)
- `featured` - Filter featured products (true/false)
- `search` - Search in name, description, category
- `ordering` - Order by price, created_at, name

Example:
```
GET /api/products/?category=1&price_min=10&price_max=100&in_stock=true&search=laptop&ordering=-price
```

## WebSocket Connections

Connect to WebSocket for real-time notifications:
```
ws://localhost:8001/ws/notifications/{user_id}/
```

## Database Models

### User Model (Extended)
- Email (unique)
- Username, First Name, Last Name
- Phone, Address, Date of Birth
- Admin flag
- Related UserProfile for additional data

### Product & Category Models
- Category: name, description, image, active status
- Product: name, description, price, stock, category, SKU, featured flag
- Optimized with database indexes

### Order System Models
- Cart & CartItem for shopping cart
- Order & OrderItem for completed orders
- Order status tracking with choices

## Caching Strategy

### Cached Data
- Product lists (1 hour TTL)
- Category lists (1 hour TTL)
- Individual product details (1 hour TTL)
- Featured products (1 hour TTL)

### Cache Invalidation
- Automatic cache clearing on product/category updates
- Cache keys are strategically designed for efficient invalidation

## Admin Interface

Access Django Admin at: `http://localhost:8000/admin/`

### Admin Features
- Complete product and category management
- Order management with status updates
- User management
- Real-time order status updates trigger WebSocket notifications

## Testing

### Sample Data Creation
Use Django Admin to create:
1. Categories (Electronics, Clothing, Books, etc.)
2. Products with various price ranges and stock levels
3. Test user accounts

### API Testing
Recommended tools:
- Postman
- curl
- Django REST Framework browsable API

### WebSocket Testing
Use browser developer tools or WebSocket testing tools to connect to:
`ws://localhost:8001/ws/notifications/{user_id}/`

## Production Deployment

### Environment Variables
Set up these environment variables for production:
```env
DEBUG=False
SECRET_KEY=your-secret-key
DB_NAME=production_db
DB_USER=db_user
DB_PASSWORD=secure_password
DB_HOST=db_host
DB_PORT=5432
REDIS_URL=redis://redis_host:6379
```

### Additional Production Setup
1. Configure CORS settings
2. Set up SSL certificates
3. Configure static file serving
4. Set up proper Redis configuration
5. Configure database connection pooling

## API Authentication

### Registration
```bash
curl -X POST http://localhost:8000/auth/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Using JWT Token
```bash
curl -X GET http://localhost:8000/auth/api/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Troubleshooting

### Common Issues

1. **Redis Connection Error**
   - Ensure Redis server is running
   - Check Redis configuration in settings

2. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check database credentials

3. **WebSocket Connection Issues**
   - Ensure Daphne is running on correct port
   - Check channel layer configuration

4. **Import Errors**
   - Ensure all dependencies are installed
   - Check virtual environment activation

### Performance Tips

1. **Database Optimization**
   - Use database indexes effectively
   - Implement query optimization with select_related/prefetch_related

2. **Caching**
   - Monitor cache hit rates
   - Adjust cache TTL based on usage patterns

3. **API Response Times**
   - Use pagination for large datasets
   - Implement API rate limiting if needed

## Support

For support or questions, please create an issue in the repository.
