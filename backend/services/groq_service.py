import json
from groq import Groq
from sqlalchemy.orm import Session
from datetime import datetime
from core.config import settings
from models.metrics import Insight
from models.player import Player
from fastapi import HTTPException
from typing import List, Dict, Any, Optional

class GroqService:
    """
    Servicio de integración con LLMs (Groq) diseñado para generar
    resúmenes e insights de coaching personalizados en formato JSON,
    basado en las prioridades detectadas.
    """
    def __init__(self, db: Session):
        self.db = db
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        
        self.system_prompt = """
        Eres un Coach Personal de League of Legends de nivel profesional, enfocado estrictamente en mejorar el rendimiento individual del jugador.
        
        Reglas de Oro que DEBES seguir:
        1. Tu trabajo principal es comunicar los hallazgos del "Motor de Prioridades" (top_priorities) al jugador, así como destacar sus aciertos en base a (top_strengths).
        2. No juzgues a los compañeros de equipo.
        3. Sé constructivo y alentador.
        4. Las "top_priorities" representan los peores defectos. Explícaselos y dale un consejo táctico accionable.
        5. Las "top_strengths" representan sus mayores logros y ventajas. En la sección "strengths", usa EXCLUSIVAMENTE los datos provistos en "top_strengths". No inventes logros que no estén ahí. Si no hay fortalezas, omite la sección o pon una general de ánimo.
        6. Habla siempre en español.
        
        DEBES responder ÚNICAMENTE con un objeto JSON válido (sin formato Markdown, solo el JSON) con la siguiente estructura exacta:
        {
            "summary": "Tu resumen general aquí, alentador y profesional.",
            "strengths": [
                {
                    "claim": "Punto fuerte detectado (basado en top_strengths)",
                    "evidence": "Evidencia extraída del contexto de top_strengths"
                }
            ],
            "priorities": [
                {
                    "title": "Tópico a mejorar (basado en top_priorities)",
                    "evidence": "Explicación del defecto y su contexto",
                    "confidence": "high",
                    "action": "Qué hacer al respecto tácticamente",
                    "success_metric": "Métrica para validar la mejora"
                }
            ],
            "next_session_plan": [
                "Plan 1",
                "Plan 2"
            ]
        }
        Asegúrate de basar tus prioridades estrictamente en las "top_priorities" proveídas.
        """

    def _build_messages(self, summary_data: Dict[str, Any], past_insights: Optional[List[Insight]] = None) -> List[Dict[str, str]]:
        """
        Construye el arreglo de mensajes (contexto, historial, y prompt actual) para enviar al LLM.
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        if past_insights and len(past_insights) > 0:
            history_context = "Aquí están los últimos consejos de coaching que recibiste anteriormente:\n"
            for past in past_insights:
                history_context += f"---\n{past.generated_analysis}\n"
            messages.append({"role": "user", "content": history_context})
            messages.append({"role": "assistant", "content": "Entendido. Emitiré mi evaluación en formato JSON estricto."})

        optimized_summary = {
            "matches_analyzed": summary_data.get("matches_analyzed", 0),
            "win_rate": summary_data.get("win_rate", 0),
            "top_priorities": summary_data.get("top_priorities", []),
            "top_strengths": summary_data.get("top_strengths", [])
        }

        prompt_content = f"Aquí tienes las nuevas métricas calculadas de las últimas {summary_data.get('matches_analyzed', 0)} partidas:\n"
        prompt_content += json.dumps(optimized_summary, indent=2)
        prompt_content += "\nGenera tu evaluación de coaching en formato JSON."
        
        messages.append({"role": "user", "content": prompt_content})
        return messages

    def _get_fallback_json(self, summary_data: Dict[str, Any]) -> str:
        """
        Genera un JSON por defecto (mock) en caso de que falle la petición a la API de Groq.
        """
        matches = summary_data.get('matches_analyzed', 0)
        win_rate = summary_data.get('win_rate', 0)
        cs_pm = summary_data.get('averages', {}).get('cs_per_min', 0)
        kp = summary_data.get('averages', {}).get('kill_participation', 0)
        deaths = summary_data.get('totals', {}).get('deaths_before_objectives', 0)

        fallback_json = {
            "summary": f"He analizado tus {matches} partidas a máxima velocidad. Tu Win Rate es de {win_rate}%. Es un buen rendimiento, aunque hay detalles tácticos por refinar.",
            "strengths": [
                {
                    "claim": "Buena economía y peleas",
                    "evidence": f"{cs_pm} CS/min y un Kill Participation de {kp}%."
                }
            ],
            "priorities": [
                {
                    "title": "Muertes perjudiciales antes de objetivos",
                    "evidence": f"{deaths} muertes en la ventana de 30-70 segundos antes de un objetivo.",
                    "confidence": "high",
                    "action": "No luches sin visión si el temporizador del objetivo está por expirar.",
                    "success_metric": "0 muertes antes de objetivos en las próximas 3 partidas"
                }
            ],
            "next_session_plan": [
                "Evitar morir 1 minuto antes de que salga el dragón",
                "Comprar un Pink Ward antes de objetivos importantes"
            ]
        }
        return json.dumps(fallback_json)

    def _call_llm(self, messages: List[Dict[str, str]], summary_data: Dict[str, Any]) -> str:
        """
        Ejecuta la solicitud a la API de Groq y maneja las excepciones si ocurren,
        devolviendo el JSON en crudo generado por el modelo o la respuesta de respaldo.
        """
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            raw_json_str = response.choices[0].message.content
            # Validar que es JSON correcto
            json.loads(raw_json_str)
            return raw_json_str
        except Exception as e:
            print(f"Groq API Error: {str(e)}. Utilizando respuesta de respaldo (Mock).")
            return self._get_fallback_json(summary_data)

    def generate_coaching_insight(self, player_id: str, summary_data: Dict[str, Any], past_insights: Optional[List[Insight]] = None) -> Insight:
        """
        Genera el informe de análisis (Insight) integrando todo el contexto de partidas y prioridades,
        persistiendo el resultado en la base de datos.
        """
        player = self.db.query(Player).filter(Player.id == player_id).first()
        if not player:
            raise HTTPException(status_code=404, detail="Player not found for insight generation")

        messages = self._build_messages(summary_data, past_insights)
        generated_text = self._call_llm(messages, summary_data)

        insight = Insight(
            player_id=player.id,
            period_start=datetime.now(), 
            period_end=datetime.now(),
            category="General Coaching - Groq",
            evidence_json=summary_data,
            confidence="high",
            generated_analysis=generated_text
        )
        
        self.db.add(insight)
        self.db.commit()
        self.db.refresh(insight)
        
        return insight
