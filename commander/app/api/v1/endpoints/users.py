from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from commander.app.api.dependencies import get_db, get_current_active_user
from commander.app.crud.crud_user import crud_user
from commander.app.schemas.user import UserCreate, UserResponse, User, UserUpdate
from commander.app.core.security import get_current_user, hash_password

router = APIRouter()

@router.post("/users/", response_model=UserCreate)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(user_in.password)
    db_user = User(email=user_in.email, full_name=user_in.full_name, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
@router.get("/users/me/", response_model=UserResponse)
def read_users_me(current_user: UserResponse = Depends(get_current_active_user)):
    return current_user

@router.get("/users/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}



@router.put("/users/{user_id}", response_model=UserUpdate)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud_user.update(db=db, db_obj=user, obj_in=user_in)
    return user