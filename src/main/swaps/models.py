import uuid
import enum
from datetime import datetime

from sqlalchemy import Column, ForeignKey, DateTime, Enum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.main.commons.db_configuration import Base


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

    requester = relationship("User", foreign_keys=[requester_id], back_populates="requested_shifts")
    requested = relationship("User", foreign_keys=[requested_id], back_populates="requester_shifts")
    requester_shift = relationship("Shift", foreign_keys=[requester_shift_id], back_populates="requested_swaps")
    requested_shift = relationship("Shift", foreign_keys=[requested_shift_id], back_populates="requester_swaps")
