from pydantic import BaseModel, Field
from typing import Optional


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        orm_mode = True


class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        orm_mode = True
