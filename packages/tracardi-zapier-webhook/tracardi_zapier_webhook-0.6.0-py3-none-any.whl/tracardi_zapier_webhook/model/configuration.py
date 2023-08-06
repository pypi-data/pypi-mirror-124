import json
from json import JSONDecodeError
from typing import Union, Dict

from pydantic import AnyHttpUrl, BaseModel, validator


class ZapierWebHookConfiguration(BaseModel):
    url: AnyHttpUrl
    body: Union[str, Dict] = ""
    timeout: int = 10

    @validator("body")
    def validate_content(cls, value):
        try:
            # Try parsing JSON
            return json.loads(value)
        except JSONDecodeError as e:
            raise ValueError(str(e))
