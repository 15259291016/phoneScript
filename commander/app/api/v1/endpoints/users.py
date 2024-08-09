from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# from commander.router.api.dependencies import get_db, get_current_active_user
# from commander.router.user import user
# from commander.router.user import UserCreate, UserResponse, User, UserUpdate
# from commander.router.core.security import get_current_user, hash_password

from commander.app.crud.crud_user import get_users, get_user_by_username, get_user, get_companies
from commander.app.db.session import get_db
from commander.app.schemas.user import User, UserCreate, Company, CompanyCreate

router = APIRouter()


# @router.post("/users/", response_model=UserCreate)
# def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
#     hashed_pw = hash_password(user_in.password)
#     db_user = User(email=user_in.email, full_name=user_in.full_name, hashed_password=hashed_pw)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
# @router.get("/users/me/", response_model=UserResponse)
# def read_users_me(current_user: UserResponse = Depends(get_current_active_user)):
#     return current_user
#
# @router.get("/users/me")
# def read_users_me(current_user: str = Depends(get_current_user)):
#     return {"username": current_user}
#
#
#
# @router.put("/users/{user_id}", response_model=UserUpdate)
# def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
#     user = user.get(db, id=user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user = user.update(db=db, db_obj=user, obj_in=user_in)
#     return user


@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.post("/companies/", response_model=Company)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    return create_company(db=db, company=company)


@router.get("/companies/", response_model=list[Company])
def read_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    companies = get_companies(db, skip=skip, limit=limit)
    return companies
