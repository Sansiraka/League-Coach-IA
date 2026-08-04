import json
from db.database import SessionLocal
from models.player import Player
from services.analytics_service import AnalyticsService

def test_strengths():
    db = SessionLocal()
    try:
        players = db.query(Player).all()
        if not players:
            print("No hay jugadores en la base de datos.")
            return

        analytics = AnalyticsService(db)
        
        for p in players:
            print(f"\n--- Probando jugador: {p.riot_id}#{p.tag_line} ---")
            try:
                summary = analytics.get_summary(p.riot_id, p.tag_line)
                
                print("Fortalezas (Top Strengths):")
                strengths = summary.get("top_strengths", [])
                if strengths:
                    for s in strengths:
                        print(f" - [{s['topic']}] (Impacto: {s.get('impact', 0)}): {s.get('context', '')}")
                else:
                    print(" - No se encontraron fortalezas destacadas.")
                    
                print("\nPrioridades a Mejorar (Top Priorities):")
                priorities = summary.get("top_priorities", [])
                if priorities:
                    for p_issue in priorities:
                        print(f" - [{p_issue['topic']}] (Severidad: {p_issue.get('severity', 0)}): {p_issue.get('context', '')}")
                else:
                    print(" - No se encontraron problemas graves.")
                    
            except Exception as e:
                print(f"Error procesando al jugador {p.riot_id}#{p.tag_line}: {e}")
                
    finally:
        db.close()

if __name__ == "__main__":
    test_strengths()
