from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..tables import tasks
from ..database import get_session
from ..schemas import TaskCreate,TaskOut,Pagination
from sqlalchemy import select,update,delete,insert
from typing import List,Annotated,Dict
from app.dependencies.pagination import get_pagination
from ..dependencies.current_user import get_current_user
from sqlalchemy.engine import Row

router=APIRouter(
    tags=["tasks"],
    prefix="/tasks",
    dependencies=[Depends(get_current_user)]
)

@router.get("/",response_model=List[TaskOut])
async def get_all_tasks(
    session:Annotated[AsyncSession,Depends(get_session)],
    page:Annotated[Pagination,Depends(get_pagination)],
):
    stmt=(
        select(tasks)
        .limit(page.limit)
        .offset(page.offset)
        .order_by(tasks.c.updated_at.desc())
    )
    
    result= await session.execute(stmt)
    rows=result.fetchall()
    return [
        TaskOut(id=row.id,title=row.title,description=row.description,status=row.status,created_at=row.created_at,updated_at=row.updated_at)
        for row in rows
    ]

@router.get("/{id}",response_model=TaskOut)
async def get_noteby_id(id:int,
        session:Annotated[AsyncSession,Depends(get_session)]                    
    ):
    stmt=(select(tasks)
          .where(tasks.c.id==id)
    )
    result= await session.execute(stmt)
    row=result.fetchone()
        
    if row is not None:
        return TaskOut(id=row.id,title=row.title,description=row.description,status=row.status,created_at=row.created_at,updated_at=row.updated_at)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task Not Found"
        )
    

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=TaskOut)
async def create_task(
    task:TaskCreate,session:Annotated[AsyncSession,Depends(get_session)],
    current_user:Annotated[Row,Depends(get_current_user)]
    ):

    stmt= ( 
        insert(tasks)
        .values(title=task.title,description=task.description)
        .returning(tasks.c.id,tasks.c.title,tasks.c.description,tasks.c.status,tasks.c.created_at,tasks.c.updated_at)
    )

    result= await session.execute(stmt)
    await session.commit()
    row=result.fetchone()
    return TaskOut(id=row.id,title=row.title,description=row.description,status=row.status,created_at=row.created_at,updated_at=row.updated_at)

@router.put("/{id}",response_model=TaskOut)
async def update_task(
    task:TaskCreate,id:int,session:Annotated[AsyncSession,Depends(get_session)],
    current_user:Annotated[Row,Depends(get_current_user)]
    ):
    stmt=(
        update(tasks)
        .where(tasks.c.id==id)
        .values(title=task.title,description=task.description)
        .returning(tasks.c.id,tasks.c.title,tasks.c.description,tasks.c.status,tasks.c.created_at,tasks.c.updated_at)
    )

    
    result= await session.execute(stmt)
    await session.commit()
    row=result.fetchone()
        
    
    if row is not None:
        return TaskOut(id=row.id,title=row.title,description=row.description,status=row.status,created_at=row.created_at,updated_at=row.updated_at)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task Not Found"
        )
    
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id:int,session:Annotated[AsyncSession,Depends(get_session)],
    current_user:Annotated[Row,Depends(get_current_user)]
    ):
    stmt=(
        delete(tasks)
        .where(tasks.c.id==id)
        .returning(tasks.c.id)
    )

    
    result= await session.execute(stmt)
    await session.commit()
    row=result.fetchone()
        
    
    if row is not None:
        return
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task Not Found"
        )