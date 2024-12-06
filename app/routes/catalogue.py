# routes/catalogue.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.catalogue import Catalogue, Book
from ..schemas.catalogue import CatalogueCreate, Catalogue as CatalogueSchema, Book as BookSchema, BookCreate

router = APIRouter()

@router.post("/catalogues/", response_model=CatalogueSchema)
def create_catalogue(catalogue: CatalogueCreate, db: Session = Depends(get_db)):
    db_catalogue = Catalogue(**catalogue.dict())
    db.add(db_catalogue)
    db.commit()
    db.refresh(db_catalogue)
    return db_catalogue

@router.get("/catalogues/", response_model=List[CatalogueSchema])
def list_catalogues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    catalogues = db.query(Catalogue).offset(skip).limit(limit).all()
    return catalogues

@router.get("/catalogues/{catalogue_id}", response_model=CatalogueSchema)
def get_catalogue(catalogue_id: int, db: Session = Depends(get_db)):
    catalogue = db.query(Catalogue).filter(Catalogue.id == catalogue_id).first()
    if catalogue is None:
        raise HTTPException(status_code=404, detail="Catalogue not found")
    return catalogue

@router.post("/catalogues/{catalogue_id}/books/", response_model=BookSchema)
def add_book_to_catalogue(
    catalogue_id: int,
    book: BookCreate,
    db: Session = Depends(get_db)
):
    catalogue = db.query(Catalogue).filter(Catalogue.id == catalogue_id).first()
    if catalogue is None:
        raise HTTPException(status_code=404, detail="Catalogue not found")
    
    db_book = Book(**book.dict())
    db.add(db_book)
    catalogue.books.append(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/catalogues/{catalogue_id}/books/", response_model=List[BookSchema])
def list_catalogue_books(catalogue_id: int, db: Session = Depends(get_db)):
    catalogue = db.query(Catalogue).filter(Catalogue.id == catalogue_id).first()
    if catalogue is None:
        raise HTTPException(status_code=404, detail="Catalogue not found")
    return catalogue.books

@router.delete("/catalogues/{catalogue_id}/books/{book_id}")
def remove_book_from_catalogue(
    catalogue_id: int,
    book_id: int,
    db: Session = Depends(get_db)
):
    catalogue = db.query(Catalogue).filter(Catalogue.id == catalogue_id).first()
    if catalogue is None:
        raise HTTPException(status_code=404, detail="Catalogue not found")
    
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book not in catalogue.books:
        raise HTTPException(status_code=400, detail="Book not in catalogue")
    
    catalogue.books.remove(book)
    db.commit()
    return {"message": "Book removed from catalogue"}

@router.delete("/catalogues/{catalogue_id}")
def delete_catalogue(catalogue_id: int, db: Session = Depends(get_db)):
    catalogue = db.query(Catalogue).filter(Catalogue.id == catalogue_id).first()
    if catalogue is None:
        raise HTTPException(status_code=404, detail="Catalogue not found")
    
    db.delete(catalogue)
    db.commit()
    return {"message": "Catalogue deleted successfully"}
