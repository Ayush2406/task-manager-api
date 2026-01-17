from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title:str
    description:str
    
class TaskOut(TaskCreate):
    id:int
    created_at:datetime
    updated_at:datetime