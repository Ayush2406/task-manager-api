from app.routers import tasks,auth
from fastapi import FastAPI,HTTPException
from app.core.errors import integrity_error_handler,http_error_handler,request_validation_handler
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import RequestValidationError



app=FastAPI()

app.include_router(tasks.router)
app.include_router(auth.router)
app.add_exception_handler(IntegrityError,integrity_error_handler)
app.add_exception_handler(HTTPException,http_error_handler)
app.add_exception_handler(RequestValidationError,request_validation_handler)

@app.get("/")
async def greet():
    return {"message": "Hello There"}