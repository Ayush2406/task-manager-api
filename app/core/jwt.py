from datetime import timedelta,timezone,datetime
from jose import jwt,ExpiredSignatureError,JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE = timedelta(minutes=30)

class TokenError(Exception):
    pass

class TokenExpiredError(TokenError):
    pass

class InvalidTokenError(TokenError):
    pass

def create_access_token(user_id:str)->str:
    now=datetime.now(timezone.utc)
    exp=now+ACCESS_TOKEN_EXPIRE
    
    payload={
        "sub":str(user_id),
        "iat":now,
        "exp":exp,
        "type":"access"
    }
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    
    
    return token
    
def verify_access_token(token:str)->dict:
    try:
        
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        
        return payload
    
    except ExpiredSignatureError:
        raise TokenExpiredError()
    except JWTError:
        raise InvalidTokenError()
        
        