from typing import List
from pydantic import BaseModel, Field
from models import OrderStatus

class ProductCreate(BaseModel):
    name: str = Field(..., example="Wireless Mouse")
    price: float = Field(..., gt=0, example=29.99)

class ProductResponse(ProductCreate):
    id: str

    class Config:
        from_attributes = True

class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0, example=2)

class OrderItemResponse(BaseModel):
    product_id: str
    product_name: str
    unit_price: float
    quantity: int
    subtotal: float

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    customer_name: str = Field(..., example="Alice Smith")
    items: List[OrderItemCreate]

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderResponse(BaseModel):
    id: str
    customer_name: str
    items: List[OrderItemResponse]
    total_amount: float
    status: OrderStatus

    class Config:
        from_attributes = True