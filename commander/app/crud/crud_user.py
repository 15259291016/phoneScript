from typing import Optional
from sqlalchemy.orm import Session
from commander.app.models.user import User
from commander.app.schemas.user import UserCreate, UserUpdate
from commander.app.core.security import hash_password
from commander.app.crud.base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            full_name=obj_in.full_name,
            hashed_password=hash_password(obj_in.password),
            is_active=True,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()


# 实例化 CRUDUser，并命名为 crud_user
crud_user = CRUDUser(User)
