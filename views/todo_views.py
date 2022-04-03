from typing import List

from fastapi import APIRouter
from fastapi.params import Depends

from sqlalchemy.orm import Session

from crud import todo_crud
from crud.user_crud import get_current_user
from db import get_db
from models import UserModel
from schemas.todo_schemas import TodoResponseSchema, TodoBaseSchema, TodoUpdateSchema

todo_router = APIRouter()

@todo_router.get("", response_model=List[TodoResponseSchema])
def get_my_todos_view(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    todos = todo_crud.get_user_todos(db, current_user)
    return todos

@todo_router.post("", response_model=List[TodoResponseSchema])
def add_todo(todo: TodoBaseSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    todo_crud.add_todo(db, current_user, todo)
    todos = todo_crud.get_user_todos(db, current_user)
    return todos

@todo_router.put("", response_model=List[TodoResponseSchema])
def update_todo(todo: TodoUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    todo_crud.update_todo(db, new_todo=todo)
    todos = todo_crud.get_user_todos(db, current_user)
    return todos

@todo_router.delete("/{todo_id:int}", response_model=List[TodoResponseSchema])
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    todo_crud.delete_todo(db, todo_id)
    todos = todo_crud.get_user_todos(db, current_user)
    return todos
