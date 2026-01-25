from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import UserOut,UserLogin,UserRegister
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
async def register_user(user: UserRegister,session:Annotated[AsyncSession,Depends(get_session)]):
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

@router.post("/login",status_code=status.HTTP_200_OK)
async def authenticate_user(user:UserLogin,session:Annotated[AsyncSession,Depends(get_session)]):
    
    fake_hash="$2b$12$C6UzMDM.H6dfI/f/IKcEe."
    
    stmt=(
        select(users)
        .where(users.c.email==user.email.lower())
    )
    result=await session.execute(stmt)
    row=result.fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
        
    hashed= row.hashed_password if row else fake_hash
    
    password_valid=verify_password(user.password,hashed)
    
    if password_valid==False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    return {
        "id":row.id,
        "email":row.email
    }