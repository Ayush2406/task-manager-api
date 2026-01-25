from datetime import timedelta,timezone,datetime
from jose import jwt,ExpiredSignatureError,JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE = timedelta(minutes=30)


def create_access_token(user_id:str)->str:
    now=datetime.now(timezone.utc)
    exp=now+ACCESS_TOKEN_EXPIRE
    
    payload={
        "sub":str(user_id),
        "exp":exp
    }
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    
    
    return token
    
def verify_access_token(token:str)->str:
    try:
        
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id=payload.get("sub")
        
        if user_id is None:
            raise RuntimeError("Token payload missing 'sub'")
        
        return user_id
    
    except ExpiredSignatureError:
        raise RuntimeError("Token was Expired")
    except JWTError:
        raise RuntimeError("Invalid Token")
        
        