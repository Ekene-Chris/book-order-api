# models/book_order.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from ..database import Base

class BookOrder(Base):
    __tablename__ = "book_orders"

    id = Column(Integer, primary_key=True, index=True)
    book_title = Column(String, index=True)
    customer_name = Column(String)
    quantity = Column(Integer)
    total_price = Column(Float)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")
