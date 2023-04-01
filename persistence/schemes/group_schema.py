from uuid import UUID

from pydantic import BaseModel
from pydantic.schema import datetime


class GroupCreate(BaseModel):
    name: str
    description: str


class GroupRead(BaseModel):
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
