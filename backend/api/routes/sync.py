from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from services.sync_service import SyncService

router = APIRouter(prefix="/sync", tags=["sync"])

@router.post("/{game_name}/{tag_line}")
async def sync_matches(game_name: str, tag_line: str, db: Session = Depends(get_db)):
    service = SyncService(db)
    result = await service.sync_player_matches(game_name, tag_line)
    return result
