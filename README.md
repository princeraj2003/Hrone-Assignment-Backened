# E-commerce API - Testing Guide

Welcome to the E-commerce API! This guide will walk you through testing each API endpoint using the deployed application.

## 🚀 Live API Documentation

**Deployed API**: https://hrone-backend-product-api.onrender.com/docs

**Base URL**: https://hrone-backend-product-api.onrender.com

---

## 📋 API Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/products` | Create a new product |
| GET | `/api/v1/products` | Get all products with filtering |
| POST | `/api/v1/orders` | Create a new order |
| GET | `/api/v1/orders/{user_id}` | Get orders for a specific user |
<img width="1919" height="964" alt="image" src="https://github.com/user-attachments/assets/4e7cdb6c-0e6a-4cb6-8a46-72ceb123fa9f" />


---

## 🛍️ Product Management

### 1. Create Product

**Endpoint**: `POST /api/v1/products`

**Request Body**:
```json
{
  "name": "Premium T-Shirt",
  "size": "large",
  "price": 299.99,
  "quantity": 50
}
```

**Expected Response (201 Created)**:
```json
{
  "name": "Premium T-Shirt",
  "size": "large",
  "price": 299.99,
  "quantity": 50,
  "id": "60f7b3b3b3b3b3b3b3b3b3b3"
}
```

**Screenshot Placeholder**:

<img width="1919" height="979" alt="image" src="https://github.com/user-attachments/assets/ede80d3e-e6b0-42f9-9533-543c7bb4b89b" />
<img width="1919" height="791" alt="image" src="https://github.com/user-attachments/assets/964a92bc-71f3-458a-8d21-449f8f7e47f7" />

### 2. Get All Products

**Endpoint**: `GET /api/v1/products`

**Query Parameters** (all optional):
- `name`: Search by product name (partial match)
- `size`: Filter by size
- `limit`: Number of products to return (default: 10)
- `offset`: Number of products to skip (default: 0)

**Examples**:

#### Get All Products
```bash
curl "https://hrone-backend-product-api.onrender.com/api/v1/products"
```

#### Search by Name
```bash
curl "https://hrone-backend-product-api.onrender.com/api/v1/products?name=shirt"
```

#### Filter by Size with Pagination
```bash
curl "https://hrone-backend-product-api.onrender.com/api/v1/products?size=large&limit=5&offset=0"
```

**Expected Response (200 OK)**:
```json
{
  "products": [
    {
      "name": "T-shirt",
      "size": "large",
      "price": 299.99,
      "quantity": 20,
      "_id": "687a825c2f0645e8313cf8ac"
    },
    {
      "name": "Denim Jeans",
      "size": "large",
      "price": 899.5,
      "quantity": 25,
      "_id": "687a832b2f0645e8313cf8ae"
    }
  ],
  "total": 2,
  "offset": 0,
  "limit": 10
}
```

**Screenshot Placeholder**:
<img width="1919" height="792" alt="image" src="https://github.com/user-attachments/assets/87387a07-acfa-4e69-a187-f904b6195b62" />
<img width="1919" height="801" alt="image" src="https://github.com/user-attachments/assets/bd05db7c-a010-4c38-b647-556a423fdce6" />


---

## 🛒 Order Management

### 3. Create Order

**Endpoint**: `POST /api/v1/orders`

**Request Body**:
```json
{
  "user_id": "user123",
  "products": [
    {
      "product_id": "60f7b3b3b3b3b3b3b3b3b3b3",
      "quantity": 2
    },
    {
      "product_id": "60f7b3b3b3b3b3b3b3b3b3b4",
      "quantity": 1
    }
  ]
}
```

**cURL Example**:
```bash
curl -X POST "https://hrone-backend-product-api.onrender.com/api/v1/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "products": [
      {
        "product_id": "60f7b3b3b3b3b3b3b3b3b3b3",
        "quantity": 2
      }
    ]
  }'
```

**Expected Response (201 Created)**:
```json
{
  "user_id": "user123",
  "products": [
    {
      "product_id": "60f7b3b3b3b3b3b3b3b3b3b3",
      "quantity": 2
    }
  ],
  "id": "60f7b3b3b3b3b3b3b3b3b3b5",
  "created_at": "2025-07-18T10:30:00.000Z"
}
```

**Screenshot Placeholder**:
<img width="1660" height="785" alt="image" src="https://github.com/user-attachments/assets/e9415bf0-ccfd-44f6-836b-dfabafdfec80" />
<img width="1864" height="810" alt="image" src="https://github.com/user-attachments/assets/1d507eb5-f7a3-4891-81d7-8a369ae7dbda" />



---

### 4. Get User Orders

**Endpoint**: `GET /api/v1/orders/{user_id}`

**Path Parameters**:
- `user_id`: The ID of the user

**Query Parameters** (optional):
- `limit`: Number of orders to return (default: 10)
- `offset`: Number of orders to skip (default: 0)

**Examples**:

#### Get All Orders for User
```bash
curl "https://hrone-backend-product-api.onrender.com/api/v1/orders/user123"
```

#### Get Orders with Pagination
```bash
curl "https://hrone-backend-product-api.onrender.com/api/v1/orders/user123?limit=5&offset=0"
```

**Expected Response (200 OK)**:
```json
{
  "orders": [
    {
      "user_id": "user123",
      "products": [
        {
          "product_id": "60f7b3b3b3b3b3b3b3b3b3b3",
          "quantity": 2
        }
      ],
      "id": "60f7b3b3b3b3b3b3b3b3b3b5",
      "created_at": "2025-07-18T10:30:00.000Z"
    }
  ],
  "total": 1,
  "offset": 0,
  "limit": 10
}
```

**Screenshot Placeholder**:
<img width="1919" height="700" alt="image" src="https://github.com/user-attachments/assets/43b839b0-f2e0-49a1-ba07-8d8f50f2c949" />
<img width="1916" height="825" alt="image" src="https://github.com/user-attachments/assets/64f104ce-ea67-4e53-a783-8060f99b6279" />



---

Happy coding! 🚀
