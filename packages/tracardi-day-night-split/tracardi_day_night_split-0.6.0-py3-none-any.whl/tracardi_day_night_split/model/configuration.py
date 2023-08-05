from pydantic import BaseModel


class Configuration(BaseModel):
    timezone: str
