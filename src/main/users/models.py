import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.main.commons.db_configuration import Base
from src.main.groups.models import UserGroup
from src.main.swaps.models import ShiftSwap


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    groups = relationship("Group", secondary=UserGroup.__tablename__, back_populates="users")
    requested_shifts = relationship("ShiftSwap", foreign_keys=ShiftSwap.requester_id, back_populates="requester")
    requester_shifts = relationship("ShiftSwap", foreign_keys=ShiftSwap.requested_id, back_populates="requested")
