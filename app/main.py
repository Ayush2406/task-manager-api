from app.routers import tasks
from fastapi import FastAPI

app=FastAPI()

app.include_router(tasks.router)

@app.get("/")
async def greet():
    return {"message": "Hello There"}