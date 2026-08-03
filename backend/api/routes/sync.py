from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from services.sync_service import SyncService
from models.player import Player

router = APIRouter(prefix="/sync", tags=["sync"])

@router.get("/testdb")
async def test_db(db: Session = Depends(get_db)):
    try:
        player = db.query(Player).first()
        return {"status": "ok", "player": player.riot_id if player else None}
    except Exception as e:
        import traceback
        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}

@router.post("/{game_name}/{tag_line}")
async def sync_matches(game_name: str, tag_line: str, db: Session = Depends(get_db)):
    try:
        service = SyncService(db)
        result = await service.sync_player_matches(game_name, tag_line)
        return result
    except Exception as e:
        import traceback
        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}
