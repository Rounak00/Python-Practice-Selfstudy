from fastapi import APIRouter, HTTPException, Query, Path
from app.models.todo_model import Todo
from app.schemas.todo_schema import TodoCreate, TodoUpdate
from typing import List

router = APIRouter(prefix="/todos", tags=["Todos"])

# ✅ Create Todo
@router.post("/", response_model=Todo)
async def create_todo(todo_data: TodoCreate):
    todo = Todo(**todo_data.dict())
    await todo.insert()
    return todo

# 📋 Get All Todos (with optional query params)
@router.get("/", response_model=List[Todo])
async def get_todos(is_completed: bool | None = Query(None, description="Filter by completion status")):
    if is_completed is not None:
        todos = await Todo.find(Todo.is_completed == is_completed).to_list()
    else:
        todos = await Todo.find_all().to_list()
    return todos

# 🔍 Get Single Todo by ID
@router.get("/{todo_id}", response_model=Todo)
async def get_todo(todo_id: str = Path(..., description="Todo ID")):
    todo = await Todo.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# ✏️ Update Todo
@router.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo_update: TodoUpdate):
    todo = await Todo.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_data = todo_update.dict(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(todo, key, value)

    await todo.save()
    return todo

# ❌ Delete Todo
@router.delete("/{todo_id}")
async def delete_todo(todo_id: str):
    todo = await Todo.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    await todo.delete()
    return {"message": "Todo deleted successfully"}
