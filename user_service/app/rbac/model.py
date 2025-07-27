# user_service/app/rbac/model.py

import uuid
from sqlalchemy import Column, String, Boolean, Integer, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from user_service.app.common.db import Base 
import enum



class UserRole(enum.Enum):
    admin = "admin"
    customer = "customer"
    field_exec = "field_exec"


class UserPagePermission(Base):
    __tablename__ = "user_page_permissions"
    __table_args__ = {"schema": "user_service"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(
    Enum(UserRole, name="user_role", schema="user_service"), nullable=False)
    label = Column(String, nullable=False)
    is_submenu = Column(Boolean, default=False)
    parent_label = Column(String, nullable=True)
    order = Column(Integer, nullable=True)
    icon_class = Column(Text, nullable=True)
    href = Column(String, nullable=True)
