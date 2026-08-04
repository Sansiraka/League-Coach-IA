import asyncio
import json
from db.database import SessionLocal
from models.player import Player
from services.analytics_service import AnalyticsService
from services.groq_service import GroqService

def test_groq():
    db = SessionLocal()
    try:
        player = db.query(Player).filter(Player.riot_id == "Sansi", Player.tag_line == "LAN").first()
        if not player:
            print("Jugador no encontrado.")
            return

        print(f"Generando resumen analítico para {player.riot_id}#{player.tag_line}...")
        analytics = AnalyticsService(db)
        summary = analytics.get_summary(player.riot_id, player.tag_line)

        print("Llamando a Groq para generar el Coaching Insight...")
        groq_service = GroqService(db)
        insight = groq_service.generate_coaching_insight(player.id, summary)

        print("\n=== RESPUESTA GENERADA POR EL COACH IA (GROQ) ===\n")
        parsed_json = json.loads(insight.generated_analysis)
        print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_groq()
