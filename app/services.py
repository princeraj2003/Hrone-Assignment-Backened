from typing import List, Optional, Tuple
from bson import ObjectId
from datetime import datetime
from app.database import get_database
from app.schemas import ProductCreate, ProductResponse, OrderCreate, OrderResponse
import re


class ProductService:
    @staticmethod
    async def create_product(product: ProductCreate) -> ProductResponse:
        db = await get_database()
        
        product_dict = product.model_dump()
        result = await db.products.insert_one(product_dict)
        
        created_product = await db.products.find_one({"_id": result.inserted_id})
        created_product["_id"] = str(created_product["_id"])
        return ProductResponse(**created_product)
    
    @staticmethod
    async def get_products(
        name: Optional[str] = None,
        size: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[List[ProductResponse], int]:
        db = await get_database()
        
        # Build query filter
        filter_query = {}
        
        if name:
            # Support partial and regex search
            filter_query["name"] = {"$regex": name, "$options": "i"}
        
        if size:
            filter_query["size"] = size
        
        # Get total count
        total = await db.products.count_documents(filter_query)
        
        # Get products with pagination, sorted by _id
        cursor = db.products.find(filter_query).sort("_id", 1).skip(offset).limit(limit)
        products = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string for each product
        for product in products:
            product["_id"] = str(product["_id"])
        
        return [ProductResponse(**product) for product in products], total
    
    @staticmethod
    async def get_product_by_id(product_id: str) -> Optional[ProductResponse]:
        db = await get_database()
        
        if not ObjectId.is_valid(product_id):
            return None
            
        product = await db.products.find_one({"_id": ObjectId(product_id)})
        
        if product:
            product["_id"] = str(product["_id"])
            return ProductResponse(**product)
        return None


class OrderService:
    @staticmethod
    async def create_order(order: OrderCreate) -> OrderResponse:
        db = await get_database()
        
        # Validate that all products exist and have sufficient quantity
        for order_product in order.products:
            if not ObjectId.is_valid(order_product.product_id):
                raise ValueError(f"Invalid product ID: {order_product.product_id}")
                
            product = await db.products.find_one({"_id": ObjectId(order_product.product_id)})
            
            if not product:
                raise ValueError(f"Product not found: {order_product.product_id}")
            
            if product["quantity"] < order_product.quantity:
                raise ValueError(f"Insufficient quantity for product: {order_product.product_id}")
        
        # Create order
        order_dict = order.model_dump()
        order_dict["created_at"] = datetime.utcnow()
        
        result = await db.orders.insert_one(order_dict)
        
        # Update product quantities
        for order_product in order.products:
            await db.products.update_one(
                {"_id": ObjectId(order_product.product_id)},
                {"$inc": {"quantity": -order_product.quantity}}
            )
        
        created_order = await db.orders.find_one({"_id": result.inserted_id})
        created_order["_id"] = str(created_order["_id"])
        return OrderResponse(**created_order)
    
    @staticmethod
    async def get_user_orders(
        user_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[List[OrderResponse], int]:
        db = await get_database()
        
        filter_query = {"user_id": user_id}
        
        # Get total count
        total = await db.orders.count_documents(filter_query)
        
        # Get orders with pagination, sorted by _id
        cursor = db.orders.find(filter_query).sort("_id", 1).skip(offset).limit(limit)
        orders = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string for each order
        for order in orders:
            order["_id"] = str(order["_id"])
        
        return [OrderResponse(**order) for order in orders], total
