from pydantic import BaseModel
from typing import Optional

class RemoveItemRequest(BaseModel):
    product_id: int

class CartItemRequest(RemoveItemRequest):
    quantity: int

class VoucherRequest(BaseModel):
    voucher: str