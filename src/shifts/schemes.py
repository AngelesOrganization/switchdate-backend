from pydantic import BaseModel


class CreateShift(BaseModel):
    group_id: str
    start_time: float
    end_time: float
