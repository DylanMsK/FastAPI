from pathlib import Path

from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel

from src.config import settings
from src.middlewares import CustomMiddleware
from src.route import BaseAPIRoute
from src.custom_logging import CustomizeLogger
from src import exception_handlers
from src.response import ErrorResponse, Response
from src.todos.router import router as todo_router


config_path = Path(__file__).with_name("logging_config.json")

app = FastAPI(
    **settings.APP_CONFIG.dict(),
    responses={
        422: {"model": ErrorResponse},
    },
)
app.logger = CustomizeLogger.make_logger(config_path)

app.add_middleware(CustomMiddleware)

app.add_exception_handler(StarletteHTTPException, exception_handlers.custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, exception_handlers.request_validation_exception_handler)

router = APIRouter(route_class=BaseAPIRoute)


@app.on_event("startup")
async def startup_event():
    # set_logger()
    pass


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


class Item(BaseModel):
    title: str
    desc: str


@app.post("/origin")
def origin(data: Item):
    return data.dict()


@router.post("/post-test", response_model=Response[Item])
def post_test(data: Item):
    return Response[Item](data=data)


# app.include_router(router)
app.include_router(todo_router)
