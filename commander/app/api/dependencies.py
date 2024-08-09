# dependencies.py 文件通常用于存放 FastAPI 应用中常用的依赖项定义。
# 依赖项是指可以在请求处理的不同阶段被复用的逻辑代码，通过 FastAPI 的 Depends 装饰器来实现注入。
# 通常，这些依赖项包括（但不限于）认证、数据库会话管理、配置获取等功能。
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Generator
from jose import JWTError, jwt

from commander.app.db.session import SessionLocal
from commander.app.core.config import settings
from commander.app.core.security import oauth2_scheme
from commander.app.models.user import User
from commander.app.crud.crud_user import crud_user

# 获取数据库会话
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 获取当前用户
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud_user.get(db, id=user_id)
    if user is None:
        raise credentials_exception
    return user

# 获取当前活动用户（已认证）
def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

# 用于抛出认证异常
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
