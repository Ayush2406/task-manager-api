from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from fastapi import Request,HTTPException
from fastapi.exceptions import RequestValidationError

async def integrity_error_handler(request:Request,exc:IntegrityError):
    error_msg=str(exc.orig)
    if "tasks_title_not_empty" in error_msg:

        return JSONResponse(
            status_code=400,
            content={
                "error":"Invalid_input",
                "message":"Title cannot be empty"
            }
        )
    elif "tasks_description_not_empty" in error_msg:
        return JSONResponse(
            status_code=400,
            content={"error_code":"Invalid_input",
                     "message":"Description cannot be empty"}
        )
    elif "users_email_key" in error_msg:
        return JSONResponse(
            status_code=409,
            content={
                "error_code":"Email already registered",
                "message":"An account with this email already exists. Please use a different email or try logging in."
            }
        )


async def http_error_handler(request:Request,exc:HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code":exc.status_code,
            "message":exc.detail
        }
    )
    
async def request_validation_handler(request:Request,exc:RequestValidationError):
    first_error=exc.errors()[0]
    
    message=first_error["msg"]
    location=first_error["loc"]
    
    field=location[-1]
    
    return JSONResponse(
        status_code=422,
        content={
            "error_code":422,
            "message":f"{field}: {message}"
        }
    )