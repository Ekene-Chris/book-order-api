# main.py
from fastapi import FastAPI
from .routes import book_order, catalogue
from .database import engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bookstore API")

# Include the router
app.include_router(book_order.router, prefix="/api/v1", tags=["orders"])
app.include_router(catalogue.router, prefix="/api/v1", tags=["catalogues"])