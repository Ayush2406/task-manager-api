from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import UserCreate, UserOut
from ..database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert,update
from ..tables import users
from ..core.security import hash_password,verify_password
from typing import Annotated

router = APIRouter(
    tags=["auth"],
    prefix="/auth"
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register_user(user: UserCreate,session:Annotated[AsyncSession,Depends(get_session)]):
    hash_pass=hash_password(user.password)
    stmt=(
        insert(users)
        .values(email=user.email.lower(),hashed_password=hash_pass)
        .returning(users.c.id,users.c.email)
    )
    result=await session.execute(stmt)
    row=result.fetchone()
    await session.commit()
    
    return UserOut(id=row.id,email=row.email)

@router.post("/login",status_code=status.HTTP_202_ACCEPTED)
async def authenticate_user(user:UserCreate,session:Annotated[AsyncSession,Depends(get_session)]):
    
    
    stmt=(
        select(users)
        .where(users.c.email==user.email)
    )
    result=await session.execute(stmt)
    row=result.fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
        
    hash_pass=verify_password(user.password,row.hashed_password)
    if hash_pass==False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    return {
        "Autentication":"Success"
    }