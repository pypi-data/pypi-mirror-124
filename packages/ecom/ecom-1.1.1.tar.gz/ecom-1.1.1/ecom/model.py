from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from db.db import Base, engine


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    p_name = Column(String(25))
    p_price = Column(Float)
    p_dec = Column(String(100))
    category_id = Column(Integer, ForeignKey("categories.id"))
    categoryFK = relationship("Category", back_populates="productFK", uselist=False)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(25))
    cat_desc = Column(String(500))
    productFK = relationship("Product", back_populates="categoryFK") #, cascade="all, delete-orphan"


