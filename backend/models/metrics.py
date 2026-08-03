import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from db.database import Base

class PlayerMatchMetrics(Base):
    __tablename__ = "player_match_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = Column(String, ForeignKey("matches.match_id"), index=True, nullable=False)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), index=True, nullable=False)
    champion = Column(String, nullable=False)
    role = Column(String)
    win = Column(Boolean)
    
    cs_per_min = Column(Float)
    gold_per_min = Column(Float)
    vision_per_min = Column(Float)
    kill_participation = Column(Float)
    deaths_before_objectives = Column(Integer, default=0)
    
    team_damage_percentage = Column(Float)
    damage_mitigated = Column(Float)
    heal_shield_effective = Column(Float)
    cc_time = Column(Float)
    turret_plates = Column(Integer, default=0)
    
    gold_diff_10 = Column(Float)
    gold_diff_15 = Column(Float)
    gold_diff_25 = Column(Float)
    
    # Métricas de visión (todos los roles)
    wards_placed = Column(Integer, default=0)
    wards_killed = Column(Integer, default=0)
    vision_wards_bought = Column(Integer, default=0)
    vision_score_advantage = Column(Float)
    
    # Alerta de CS del support
    support_cs_alert = Column(String)
    
    situational_analysis_json = Column(JSONB)
    
    # Nuevas métricas avanzadas (Early Game / Linea)
    solo_kills = Column(Integer, default=0)
    lane_minions_first_10_minutes = Column(Integer, default=0)
    max_cs_advantage_on_lane_opponent = Column(Float, default=0.0)
    max_level_lead_lane_opponent = Column(Integer, default=0)
    
    # Nuevas métricas avanzadas (Jungla)
    jungle_cs_before_10_minutes = Column(Float, default=0.0)
    epic_monster_steals = Column(Integer, default=0)
    scuttle_crab_kills = Column(Integer, default=0)
    epic_monster_kills_near_enemy_jungler = Column(Integer, default=0)
    
    # Nuevas métricas avanzadas (Support / Vision)
    ward_takedowns_before_20m = Column(Integer, default=0)
    save_ally_from_death = Column(Integer, default=0)
    
    # Nuevas métricas avanzadas (Micro / Combate)
    skillshots_dodged = Column(Integer, default=0)
    skillshots_hit = Column(Integer, default=0)
    outnumbered_kills = Column(Integer, default=0)
    kills_near_enemy_turret = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Insight(Base):
    __tablename__ = "insights"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey("players.id"), index=True, nullable=False)
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    category = Column(String)  # ej. "Economy", "Survival"
    evidence_json = Column(JSONB)
    confidence = Column(String)
    generated_analysis = Column(String) # Guardará el texto que devuelva Gemini
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
