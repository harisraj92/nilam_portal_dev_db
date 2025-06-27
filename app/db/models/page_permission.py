from sqlalchemy import Column, String, Boolean, Integer, text
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

class PagePermission(Base):
    __tablename__ = "user_page_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    role = Column(String, nullable=False)
    label = Column(String, nullable=False)
    is_submenu = Column(Boolean, default=False)
    parent_label = Column(String, nullable=True)
    order = Column(Integer)
    icon_class = Column(String, nullable=True)
    href = Column(String, nullable=True)
