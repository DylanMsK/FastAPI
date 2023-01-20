from typing import Generic, TypeVar, Optional

from pydantic import BaseModel
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class Response(GenericModel, Generic[DataT]):
    data: Optional[DataT]


class Error(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: Error
