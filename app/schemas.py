from pydantic import BaseModel,EmailStr,constr,StringConstraints
from datetime import datetime
from typing_extensions import Annotated
from uuid import UUID
class TaskCreate(BaseModel):
    title:str
    description:str
    
class TaskOut(TaskCreate):
    id:int
    created_at:datetime
    updated_at:datetime
    
    
    
class Pagination(BaseModel):
    limit:int
    offset:int
    
    
class UserCreate(BaseModel):
    email:EmailStr
    password:Annotated[str, StringConstraints(min_length=8)]
    
class UserRegister(BaseModel):
    email:EmailStr
    password:Annotated[str,StringConstraints(min_length=8)]
    
class UserLogin(BaseModel):
    email:EmailStr
    password:Annotated[str,StringConstraints(min_length=8)]

class UserOut(BaseModel):
    id:UUID
    email:EmailStr
    
    