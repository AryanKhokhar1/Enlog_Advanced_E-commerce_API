# API Documentation

## Authentication

### Register User
```http
POST /auth/api/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "testuser",
  "first_name": "Test",
  "last_name": "User",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "phone": "+1234567890",
  "address": "123 Main St, City, Country"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "phone": "+1234567890",
    "address": "123 Main St, City, Country",
    "profile": {
      "avatar": "",
      "preferences": {},
      "created_at": "2025-01-08T10:00:00Z",
      "updated_at": "2025-01-08T10:00:00Z"
    }
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "message": "User registered successfully"
}
```

### Login
```http
POST /auth/api/token/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Products

### List Products (with filtering)
```http
GET /api/products/?category=1&price_min=50&price_max=500&in_stock=true&search=phone
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Smartphone Pro Max",
      "price": "999.99",
      "stock": 50,
      "category_name": "Electronics",
      "image": "https://example.com/image.jpg",
      "is_in_stock": true,
      "featured": true
    }
  ]
}
```

### Get Product Details
```http
GET /api/products/1/
Authorization: Bearer {access_token}
```

## Cart Management

### Add Item to Cart
```http
POST /api/cart/items/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```

### Get Cart
```http
GET /api/cart/
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Smartphone Pro Max",
        "price": "999.99",
        "category_name": "Electronics"
      },
      "quantity": 2,
      "total_price": "1999.98"
    }
  ],
  "total_price": "1999.98",
  "total_items": 2
}
```

## Orders

### Create Order from Cart
```http
POST /api/orders/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "shipping_address": "123 Main St, City, Country",
  "phone_number": "+1234567890",
  "notes": "Leave at door"
}
```

### Get Order History
```http
GET /api/orders/
Authorization: Bearer {access_token}
```

## WebSocket Notifications

Connect to: `ws://localhost:8001/ws/notifications/{user_id}/`

**Message Types:**
- `order_notification`: New order created
- `order_status_update`: Order status changed

**Example Messages:**
```json
{
  "type": "order_notification",
  "order_id": 1,
  "message": "Order created successfully"
}

{
  "type": "order_status_update",
  "order_id": 1,
  "old_status": "pending",
  "new_status": "shipped",
  "message": "Order #1 status updated from pending to shipped"
}
```

## Error Responses

All error responses follow this format:
```json
{
  "error": "Error message description"
}
```

Or for validation errors:
```json
{
  "field_name": ["Error message for this field"]
}
```

## Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
