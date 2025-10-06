from fastapi import FastAPI
from app.routes.todo_routes import router as todo_router
from app.db import init_db

app = FastAPI(title="FastAPI MongoDB Todo App")

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(todo_router)