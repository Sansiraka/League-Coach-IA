import uuid
from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from db.database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = Column(String, unique=True, index=True, nullable=False)
    game_creation = Column(DateTime(timezone=True))
    game_duration = Column(Integer)
    queue_id = Column(Integer, default=440)
    queue_name = Column(String)
    patch = Column(String)
    raw_match_json = Column(JSONB)
    raw_timeline_json = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
