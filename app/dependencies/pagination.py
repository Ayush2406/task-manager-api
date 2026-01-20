from fastapi import HTTPException,status
from ..schemas import Pagination
MAX_LIMIT=100


def get_pagination(limit:int=10,offset:int=0):
   
    if limit<1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit is less than 1"
        )
    elif limit>MAX_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Limit is larger than {MAX_LIMIT}"
        )
    elif offset<0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offset is smaller than 0"
        )
    else:
        return Pagination(limit=limit,offset=offset)
    
        
    

