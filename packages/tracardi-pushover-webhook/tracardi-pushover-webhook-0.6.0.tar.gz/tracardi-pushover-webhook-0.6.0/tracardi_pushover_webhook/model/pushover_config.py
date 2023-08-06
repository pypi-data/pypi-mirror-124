from pydantic import BaseModel
from tracardi.domain.named_entity import NamedEntity


class PushOverAuth(BaseModel):
    token: str
    user: str


class PushOverConfiguration(BaseModel):
    source: NamedEntity
    message: str
