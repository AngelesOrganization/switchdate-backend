import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, DateTime, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.main.commons.db_configuration import Base
from src.main.swaps.models import ShiftSwap


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    requested_swaps = relationship("ShiftSwap", foreign_keys=ShiftSwap.requester_shift_id, back_populates="requester_shift")
    requester_swaps = relationship("ShiftSwap", foreign_keys=ShiftSwap.requested_shift_id, back_populates="requested_shift")
