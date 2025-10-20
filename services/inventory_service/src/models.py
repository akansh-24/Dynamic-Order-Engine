# services/inventory_service/src/models.py
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, func
from .database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False, unique=True, index=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
