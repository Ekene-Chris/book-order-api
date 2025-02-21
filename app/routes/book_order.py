# routes/book_order.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.book_order import BookOrder
from ..schemas.book_order import BookOrderCreate, BookOrder as BookOrderSchema, BookOrderUpdate

router = APIRouter()

@router.get("/test/")
def test_endpoint():
    """
    A simple test endpoint that returns a basic message.
    
    Returns:
        dict: A dictionary containing a welcome message and status
    """
    return {
        "message": "Welcome to the Bookstore API!",
        "status": "success",
        "test": True
    }

@router.post("/orders/", response_model=BookOrderSchema)
def create_book_order(order: BookOrderCreate, db: Session = Depends(get_db)):
    db_order = BookOrder(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/orders/", response_model=List[BookOrderSchema])
def list_book_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(BookOrder).offset(skip).limit(limit).all()
    return orders

@router.put("/orders/{order_id}", response_model=BookOrderSchema)
def update_book_order(order_id: int, order: BookOrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(BookOrder).filter(BookOrder.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    for key, value in order.dict(exclude_unset=True).items():
        setattr(db_order, key, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/orders/{order_id}")
def delete_book_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(BookOrder).filter(BookOrder.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted successfully"}