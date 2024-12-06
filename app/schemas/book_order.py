# schemas/book_order.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookOrderBase(BaseModel):
    book_title: str
    customer_name: str
    quantity: int
    total_price: float
    status: str = "pending"

class BookOrderCreate(BookOrderBase):
    pass

class BookOrderUpdate(BaseModel):
    book_title: Optional[str] = None
    customer_name: Optional[str] = None
    quantity: Optional[int] = None
    total_price: Optional[float] = None
    status: Optional[str] = None

class BookOrder(BookOrderBase):
    id: int
    order_date: datetime

    class Config:
        orm_mode = True