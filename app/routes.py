from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from app.schemas import (
    ProductCreate, 
    ProductResponse, 
    ProductsListResponse,
    OrderCreate,
    OrderResponse,
    OrdersListResponse
)
from app.services import ProductService, OrderService

router = APIRouter()


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    """Create a new product"""
    try:
        return await ProductService.create_product(product)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}"
        )


@router.get("/products", response_model=ProductsListResponse)
async def get_products(
    name: Optional[str] = Query(None, description="Search products by name (partial/regex)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip")
):
    """Get list of products with optional filtering and pagination"""
    try:
        products, total = await ProductService.get_products(
            name=name,
            size=size,
            limit=limit,
            offset=offset
        )
        
        return ProductsListResponse(
            products=products,
            total=total,
            offset=offset,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching products: {str(e)}"
        )


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    """Create a new order"""
    try:
        return await OrderService.create_order(order)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating order: {str(e)}"
        )


@router.get("/orders/{user_id}", response_model=OrdersListResponse)
async def get_user_orders(
    user_id: str,
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip")
):
    """Get all orders for a specific user"""
    try:
        orders, total = await OrderService.get_user_orders(
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        
        return OrdersListResponse(
            orders=orders,
            total=total,
            offset=offset,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching orders: {str(e)}"
        )
