from fastapi import FastAPI

from src.config import get_settings
from src.middlewares import CustomHTTPMiddleware
from src.logging import set_logger

settings = get_settings()
app = FastAPI(**settings.APP_CONFIG.dict())
app.add_middleware(CustomHTTPMiddleware)


@app.on_event("startup")
async def startup_event():
    set_logger()


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck():
    return {"status": "ok"}


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
