from typing import List, Union
from pydantic import BaseModel


class GroupCreateSchema(BaseModel):
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    description: Union[str, None] = None
    tax: Union[float, None] = None
