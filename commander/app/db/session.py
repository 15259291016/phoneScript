# commander/app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from commander.app.core.config import settings

# 创建数据库引擎
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
)

# 创建数据库会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
