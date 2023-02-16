import logging
from typing import List

from fastapi import APIRouter

from src.route import BaseAPIRoute
from src.todos.schemas import Todo

logger = logging.getLogger(__name__)

todos = [
    Todo(title="Motherhood", contents="Nulla gravida vel justo eget sollicitudin."),
    Todo(title="God Save the King", contents="Sed bibendum bibendum dolor placerat cursus."),
    Todo(title="Men in Black (a.k.a. MIB)", contents="Lorem ipsum dolor sit amet, consectetur adipiscing elit."),
    Todo(title="Wild Boys of the Road", contents="Etiam ut nulla quam."),
    Todo(title="September Issue, The", contents="Donec eget dapibus libero."),
]

router = APIRouter(prefix="/todos", tags=["todos"], route_class=BaseAPIRoute)


@router.get("", response_model=List[Todo])
async def get_todo_list():
    logger.info("???")
    raise ValueError("asdfas")
    return todos


@router.post("", response_model=Todo)
async def register_todo(todo: Todo):
    todos.append(todo)
    return todo


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    return todos[todo_id]
