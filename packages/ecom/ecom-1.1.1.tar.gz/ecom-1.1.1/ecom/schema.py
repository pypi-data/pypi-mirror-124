from typing import List, Optional

from pydantic import BaseModel

class Product(BaseModel):
    p_name: str =None
    p_price: float=None
    p_dec:str =None
    class Config:
        orm_mode=True
    
class Productcreate(Product):
    category_id: int=None
    class Config:
        orm_mode=True

class Category(BaseModel):
    category: str = None
    cat_desc:str = None
    class Config:
        orm_mode=True
    