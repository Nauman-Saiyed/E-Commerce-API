from fastapi import Depends , HTTPException , status
from fastapi.security import  HTTPBearer , HTTPAuthorizationCredentials
from jose import jwt , JWTError
from app.core.config import settings

security = HTTPBearer()

def get_current_user(
    credentials : HTTPAuthorizationCredentials = Depends(security) 
):
    token = credentials.credentials
    
    try :
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
            )
        
        user_id : str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401 , detail="Invalid Token")
        return user_id
    except JWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid Token or Expired Token"
        )
        
        