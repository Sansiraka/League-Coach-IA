import uuid
from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from db.database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    puuid = Column(String, unique=True, index=True, nullable=False)
    riot_id = Column(String, nullable=False)
    tag_line = Column(String, nullable=False)
    region = Column(String, nullable=False)
    preferred_queue = Column(Integer, default=440)
    preferred_role = Column(String)
    goals_json = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
