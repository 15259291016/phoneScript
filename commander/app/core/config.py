from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = "postgresql://user:password@localhost/dbname"
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"  # JWT 使用的签名算法
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
