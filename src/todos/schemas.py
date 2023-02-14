from src.schemas import ORJSONModel


class Todo(ORJSONModel):
    title: str
    contents: str
