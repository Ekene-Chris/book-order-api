# models/catalogue.py
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.orm import relationship
from ..database import Base

# Association table for many-to-many relationship between catalogues and books
catalogue_books = Table(
    'catalogue_books',
    Base.metadata,
    Column('catalogue_id', Integer, ForeignKey('catalogues.id')),
    Column('book_id', Integer, ForeignKey('books.id'))
)

class Catalogue(Base):
    __tablename__ = "catalogues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    books = relationship("Book", secondary=catalogue_books, back_populates="catalogues")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    price = Column(Float)
    isbn = Column(String, unique=True)
    catalogues = relationship("Catalogue", secondary=catalogue_books, back_populates="books")
