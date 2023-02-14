from typing import List

from fastapi import APIRouter

from src.route import BaseAPIRoute
from src.todos.schemas import Todo


router = APIRouter(prefix="/todos", tags=["todos"], route_class=BaseAPIRoute)

todos = [
    Todo(title="Motherhood", contents="Nulla gravida vel justo eget sollicitudin."),
    Todo(title="God Save the King", contents="Sed bibendum bibendum dolor placerat cursus."),
    Todo(title="Men in Black (a.k.a. MIB)", contents="Lorem ipsum dolor sit amet, consectetur adipiscing elit."),
    Todo(title="Wild Boys of the Road", contents="Etiam ut nulla quam."),
    Todo(title="September Issue, The", contents="Donec eget dapibus libero."),
]


@router.get("", response_model=List[Todo])
def get_todo_list():
    return todos
