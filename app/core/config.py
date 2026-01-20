from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME : str = "E-Commerce-API"
    API_V1_STR: str = "/api/v1"
    
    MONGO_URL : str = "mongodb://localhost:27017"
    DB_NAME : str = "ecommerce_db"
    
    JWT_SECRET_KEY : str = "8f6d70fca64fb2ad90d5f6a8de5934783c02204f2b6ff1bdc866fcb3851a6cd8"
    JWT_ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 60 * 1
    
    OTP_EXPIRE_MINUTES : int = 5
    
    
    
settings = Settings()