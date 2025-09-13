from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func
from .database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    device_id = Column(String, unique=True, index=True)  # unique device identifier
    created_at = Column(DateTime(timezone=True), server_default=func.now())
