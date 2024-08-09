from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from commander.app.api.dependencies import get_db
from commander.app.core.security import create_access_token, verify_password
from commander.app.models.user import User
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from commander.app.services.verification import VerificationCode

router = APIRouter()
verification_code_service = VerificationCode()


@router.post("/login/")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register/")
def register_user(email: str, background_tasks: BackgroundTasks):
    code = verification_code_service.generate_code()
    verification_code_service.store_code(email, code)
    # 在这里调用发送邮件的函数，如 send_email_verification_code(email, code, background_tasks)
    return {"message": "Verification code sent"}


@router.post("/verify/")
def verify_code(email: str, code: str):
    if verification_code_service.verify_code(email, code):
        # 验证成功的逻辑，比如标记用户邮箱已验证
        return {"message": "Verification successful"}
    else:
        raise HTTPException(status_code=400, detail="Invalid or expired code")


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
