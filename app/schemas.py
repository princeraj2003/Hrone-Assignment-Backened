from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Annotated
from datetime import datetime
from bson import ObjectId


# Custom ObjectId type for Pydantic v2 compatibility
def validate_object_id(v):
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str):
        if ObjectId.is_valid(v):
            return v
        raise ValueError("Invalid ObjectId")
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[str, Field(description="MongoDB ObjectId")]


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    size: str = Field(..., min_length=1, max_length=20)
    price: float = Field(..., gt=0, le=1000000)
    quantity: int = Field(..., ge=0)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: PyObjectId = Field(alias="_id")
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    size: Optional[str] = Field(None, min_length=1, max_length=20)
    price: Optional[float] = Field(None, gt=0, le=1000000)
    quantity: Optional[int] = Field(None, ge=0)


class OrderProduct(BaseModel):
    product_id: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)


class OrderBase(BaseModel):
    user_id: str = Field(..., min_length=1)
    products: List[OrderProduct] = Field(..., min_items=1)


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: PyObjectId = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class ProductsListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    offset: int
    limit: int


class OrdersListResponse(BaseModel):
    orders: List[OrderResponse]
    total: int
    offset: int
    limit: int
