from ..core.jwt import verify_access_token
from ..database import get_session
from fastapi import status,HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..tables import users
from uuid import UUID

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token:Annotated[str,Depends(oauth2_scheme)],
    session:Annotated[AsyncSession,Depends(get_session)]
):
    try:
        user_id=UUID(verify_access_token(token=token))
        
        stmt=(
            select(users)
            .where(users.c.id==user_id)
        )
        
        result = await session.execute(stmt)
        row=result.fetchone()
        
        
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized"
            )
        return row
            
            
    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
        
        
        
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )