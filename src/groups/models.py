import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Enum
from sqlalchemy import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.commons.db_configuration import Base


class UserGroupRole(enum.Enum):
    miembro = "miembro"
    administrador = "administrador"


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"))
    role = Column(Enum(UserGroupRole), default=UserGroupRole.miembro, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow())


class Group(Base):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = relationship("User", secondary=UserGroup.__tablename__, back_populates="groups")
