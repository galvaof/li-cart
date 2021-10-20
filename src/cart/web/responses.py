from typing import List, Optional
from pydantic import BaseModel

class CartItemSchema(BaseModel):
    product_id: int
    quantity: int

class ShoppingCartSchema(BaseModel):
    id: int
    items: List[CartItemSchema]
    voucher: Optional[str]
    discount_ratio: float

class CartTotalsSchema(BaseModel):
    total: float
    subtotal: float

class CartItemDetailsSchema(BaseModel):
    product_id: int
    quantity: int
    name: str
    price: float

class ShoppingCartDetailsSchema(BaseModel):
    id: int
    items: List[CartItemDetailsSchema]
    voucher: Optional[str]
    discount: float
