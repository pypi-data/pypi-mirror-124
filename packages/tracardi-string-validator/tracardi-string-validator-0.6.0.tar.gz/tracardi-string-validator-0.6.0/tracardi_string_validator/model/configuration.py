from pydantic import BaseModel


class Configuration(BaseModel):
    validation_name: str
    data: str




