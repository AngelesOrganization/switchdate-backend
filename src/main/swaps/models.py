import uuid
import enum
from datetime import datetime

from sqlalchemy import Column, ForeignKey, DateTime, Enum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID

from src.commons.db_configuration import Base


class ShiftSwapStatus(enum.Enum):
    pendiente = "pendiente"
    aceptado = "aceptado"
    rechazado = "rechazado"


class ShiftSwap(Base):
    __tablename__ = "shift_swaps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requester_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    requested_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    requester_shift_id = Column(UUID(as_uuid=True), ForeignKey("shifts.id", ondelete="CASCADE"))
    requested_shift_id = Column(UUID(as_uuid=True), ForeignKey("shifts.id", ondelete="CASCADE"))
    status = Column(Enum(ShiftSwapStatus), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
