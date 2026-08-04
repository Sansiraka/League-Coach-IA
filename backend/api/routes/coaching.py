from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.player import Player
from models.metrics import Insight
from services.analytics_service import AnalyticsService
from services.groq_service import GroqService
from core.config import settings

router = APIRouter(prefix="/coaching", tags=["coaching"])

@router.post("/generate/{game_name}/{tag_line}")
def generate_coaching(
    game_name: str, 
    tag_line: str, 
    db: Session = Depends(get_db)
):
    player = db.query(Player).filter(Player.riot_id == game_name, Player.tag_line == tag_line).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found. Por favor sincroniza primero.")

    analytics_svc = AnalyticsService(db)
    summary = analytics_svc.get_summary(game_name, tag_line, limit=20)
    
    if summary.get("matches_analyzed", 0) == 0:
        raise HTTPException(status_code=400, detail="No hay partidas suficientes para analizar.")

    past_insights = db.query(Insight).filter(Insight.player_id == player.id).order_by(Insight.created_at.desc()).limit(2).all()
    past_insights.reverse()

    llm_svc = GroqService(db)
    insight = llm_svc.generate_coaching_insight(str(player.id), summary, past_insights=past_insights)

    import json
    import re
    
    try:
        raw = insight.generated_analysis.strip()
        # Eliminar formato markdown ```json y ``` si el modelo los añade
        if raw.startswith("```"):
            # Encontrar el primer { o [ para empezar a parsear
            start = raw.find("{")
            end = raw.rfind("}")
            if start != -1 and end != -1:
                raw = raw[start:end+1]
        
        analysis_data = json.loads(raw)
    except Exception:
        analysis_data = {"summary": "Hubo un error interpretando los datos del Coach IA. Genera de nuevo.", "strengths": [], "priorities": [], "next_session_plan": []}

    return {
        "insight_id": insight.id,
        "player": f"{game_name}#{tag_line}",
        "provider": "groq",
        "analysis": analysis_data
    }
