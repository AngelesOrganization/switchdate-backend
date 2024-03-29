from pydantic import BaseModel


class CreateSwap(BaseModel):
    requester_id: str
    requested_id: str
    requester_shift_id: str
    requested_shift_id: str
