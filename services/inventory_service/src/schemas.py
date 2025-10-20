# services/inventory_service/src/schemas.py
from pydantic import BaseModel
from datetime import datetime

class InventoryCreate(BaseModel):
    product_name: str
    quantity: int
    price: float

class InventoryBase(InventoryCreate):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True
