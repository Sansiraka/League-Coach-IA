import asyncio
from db.database import SessionLocal
from models.metrics import PlayerMatchMetrics

def test_db_metrics():
    db = SessionLocal()
    try:
        metrics = db.query(PlayerMatchMetrics).all()
        print(f"Total de registros de métricas en BD: {len(metrics)}")
        
        if not metrics:
            return
            
        saves = sum(m.save_ally_from_death or 0 for m in metrics)
        steals = sum(m.epic_monster_steals or 0 for m in metrics)
        outplays = sum(m.outnumbered_kills or 0 for m in metrics)
        dodges = sum(m.skillshots_dodged or 0 for m in metrics)
        
        print(f"Total saves across all games: {saves}")
        print(f"Total epic monster steals: {steals}")
        print(f"Total outnumbered kills: {outplays}")
        print(f"Total skillshots dodged: {dodges}")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_db_metrics()
