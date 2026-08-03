from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.database import get_db
from services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary/{game_name}/{tag_line}")
def get_analytics_summary(
    game_name: str, 
    tag_line: str, 
    limit: int = Query(20, description="Número de partidas a analizar"),
    db: Session = Depends(get_db)
):
    service = AnalyticsService(db)
    return service.get_summary(game_name, tag_line, limit)
