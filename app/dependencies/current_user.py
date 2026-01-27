from ..core.jwt import verify_access_token,TokenError
from ..database import get_session
from fastapi import status,HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..tables import users
from uuid import UUID
from ..schemas import UserOut


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")


    

async def get_current_user(
    token:Annotated[str,Depends(oauth2_scheme)],
    session:Annotated[AsyncSession,Depends(get_session)]
)->UserOut:
    try:
        payload=verify_access_token(token=token)
    except TokenError:
        raise HTTPException(status_code=401, detail="Unauthorized")

    
    sub=payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Unauthorized")

        
    try:
        user_id=UUID(sub)
    except ValueError:
       raise HTTPException(status_code=401, detail="Unauthorized")

    
    stmt=(select(users.c.id,users.c.email).where(users.c.id==user_id))
    result= await session.execute(stmt)
    row=result.fetchone()
    
    if row is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    
    return UserOut(id=row.id,email=row.email)
    
    
    
    
    
  