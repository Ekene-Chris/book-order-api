# schemas/catalogue.py
from pydantic import BaseModel
from typing import List, Optional
from ..models.catalogue import Book

class BookBase(BaseModel):
    title: str
    author: str
    price: float
    isbn: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    
    class Config:
        orm_mode = True

class CatalogueBase(BaseModel):
    name: str
    description: Optional[str] = None

class CatalogueCreate(CatalogueBase):
    pass

class Catalogue(CatalogueBase):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True