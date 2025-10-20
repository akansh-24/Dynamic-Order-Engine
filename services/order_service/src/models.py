from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, default="Pending", nullable=False)