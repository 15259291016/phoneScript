from sqlalchemy import Column, String, Boolean, Integer
from pydantic import BaseModel, EmailStr
from typing import Optional
import enum
from commander.app.db.base_class import Base


class RoleEnum(str, enum.Enum):
    super_admin = "super_admin"
    admin = "admin"
    user = "user"

class UserBase(BaseModel):
    username: str
    email: str
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    company_id: Optional[int]

    class Config:
        orm_mode = True

class CompanyBase(BaseModel):
    name: str
    address: Optional[str]

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    is_email_verified = Column(Boolean, default=False)
    is_phone_verified = Column(Boolean, default=False)
    hashed_password = Column(String)


# class UserCreate(BaseModel):
#     email: EmailStr
#     full_name: Optional[str] = None
#     password: str
#
#     class Config:
#         orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True
