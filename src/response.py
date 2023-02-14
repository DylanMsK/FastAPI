from typing import Generic, TypeVar, Optional, List

from pydantic import BaseModel
from pydantic.generics import GenericModel

Model = TypeVar("Model", bound=BaseModel)


class Response(GenericModel, Generic[Model]):
    data: Optional[Model]


class PaginatedResponse(GenericModel, Generic[Model]):
    total: int
    page: int = 1
    size: int = 10
    data: List[Model]


class Error(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: Error
