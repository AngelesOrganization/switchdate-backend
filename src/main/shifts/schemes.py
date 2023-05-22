from datetime import datetime

from pydantic import BaseModel


class CreateShift(BaseModel):
    start_time: datetime
    end_time: datetime
