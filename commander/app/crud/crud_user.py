from typing import Optional
from sqlalchemy.orm import Session
from commander.app.models.user import User
from commander.app.schemas.user import UserCreate, UserUpdate, Company, CompanyCreate
from commander.app.core.security import hash_password
from commander.app.crud.base import CRUDBase


# class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
#     def create(self, db: Session, obj_in: UserCreate) -> User:
#         db_obj = User(
#             email=obj_in.email,
#             full_name=obj_in.full_name,
#             hashed_password=hash_password(obj_in.password),
#             is_active=True,
#         )
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj
#
#     def get_by_email(self, db: Session, email: str) -> Optional[User]:
#         return db.query(User).filter(User.email == email).first()
#
#
# # 实例化 CRUDUser，并命名为 crud_user
# crud_user = CRUDUser(User)


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,  # 注意：实际中应对密码进行哈希处理
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_companies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Company).offset(skip).limit(limit).all()

def create_company(db: Session, company: CompanyCreate):
    db_company = Company(name=company.name, address=company.address)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company