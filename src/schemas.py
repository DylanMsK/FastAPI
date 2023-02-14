from datetime import datetime
from typing import Any, Callable, Optional, Dict
import pytz

import orjson
from pydantic import BaseModel, root_validator


def orjson_dumps(v: Any, *, default: Optional[Callable[[Any], Any]]) -> str:
    return orjson.dumps(v, default=default).decode()


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=pytz.UTC)

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {datetime: convert_datetime_to_gmt}
        allow_population_by_field_name = True

    @root_validator()
    def set_null_microseconds(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        datetime_fields = {k: v.replace(microsecond=0) for k, v in data.items() if isinstance(k, datetime)}

        return {**data, **datetime_fields}
