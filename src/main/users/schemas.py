from datetime import datetime
from typing import List

from pydantic import BaseModel
from uuid import UUID


from src.main.swaps.models import ShiftSwapStatus


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Shift(BaseModel):
    id: UUID
    user_id: UUID
    start_time: datetime
    end_time: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ShiftSwap(BaseModel):
    id: UUID
    requester: User
    requested: User
    requester_shift: Shift
    requested_shift: Shift
    status: ShiftSwapStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ShiftSwapList(BaseModel):
    swaps: List[ShiftSwap]
