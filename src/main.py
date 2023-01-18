from typing import Union, Dict

from fastapi import FastAPI
from pydantic import BaseModel

from src.config import settings

app = FastAPI(**settings.APP_CONFIG.dict())

print(settings)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}
