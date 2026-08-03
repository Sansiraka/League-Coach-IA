from typing import List, Dict, Any
from services.champion_archetype_service import ChampionArchetypeService

class PriorityEngine:
    """
    Motor de prioridades encargado de analizar las métricas y determinar
    cuáles son los errores más críticos que el jugador debe corregir, ordenándolos por severidad.
    """
    def __init__(self):
        # Inicializa los pesos base para errores globales y los pesos dinámicos por rol.
        self.archetype_service = ChampionArchetypeService()
        self.weights = {
            "SITUATIONAL_ERROR": 15,      # Gravedad por cada partida sin la itemización correcta
            "DEATH_BEFORE_OBJ": 20,       # Gravedad por cada muerte antes de un objetivo clave
            "LANE_DOMINATED": -30,        # Bonificación por dominar la fase de líneas
            "JUNGLE_DOMINATED": -30,      # Bonificación por asegurar el juego temprano en jungla
            "SUPPORT_SAVIOR": -25,        # Bonificación por salvar aliados de la muerte
            "MECHANICAL_GOD": -20,        # Bonificación por altas mecánicas (esquivar/acertar habilidades)
            "OUTPLAY": -15                # Bonificación por conseguir asesinatos en inferioridad numérica
        }

        # Pesos dinámicos por rol para las métricas de rendimiento.
        # Definen el impacto y la gravedad de fallar en una métrica específica dependiendo de la posición jugada.
        self.role_weights = {
            "BOTTOM": {
                "cs_per_min": 50,         # [Tirador] El farmeo es la principal fuente de oro y es crítico.
                "vision_per_min": 15,     # [Tirador] La visión es secundaria comparada con el soporte.
                "kill_participation": 30  # [Tirador] Importante para asegurar daño en peleas grupales.
            },
            "MIDDLE": {
                "cs_per_min": 45,         # [Carril Central] Muy importante para escalar.
                "vision_per_min": 20,     # [Carril Central] Controlar la visión alrededor del carril central es clave.
                "kill_participation": 35  # [Carril Central] Vital para rotaciones y peleas por objetivos.
            },
            "TOP": {
                "cs_per_min": 40,         # [Carril Superior] Importante para duelos y empuje dividido.
                "vision_per_min": 20,     # [Carril Superior] Necesario para evitar emboscadas.
                "kill_participation": 25  # [Carril Superior] Menor peso debido al empuje dividido (split push).
            },
            "JUNGLE": {
                "cs_per_min": 25,         # [Jungla] Depende del campeón, pero el impacto en el mapa suele ser mayor.
                "vision_per_min": 35,     # [Jungla] Muy importante para el control de objetivos y rastreo del jungla enemigo.
                "kill_participation": 45  # [Jungla] Crítico; su rol principal es habilitar asesinatos mediante emboscadas.
            },
            "UTILITY": {
                "cs_per_min": 0,          # [Soporte] No deben farmear, por lo que no tiene peso.
                "vision_per_min": 50,     # [Soporte] El control de visión es su principal responsabilidad; crítico.
                "kill_participation": 40  # [Soporte] Muy importante en asistencias y protección en peleas grupales.
            },
            "UNKNOWN": {
                "cs_per_min": 30,
                "vision_per_min": 30,
                "kill_participation": 30
            }
        }

    def _evaluate_situational_errors(self, summary_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evalúa y penaliza las faltas en itemización situacional (ej. falta de corta curaciones).
        """
        issues = []
        situational_errors = summary_data.get("totals", {}).get("situational_errors", {})
        for error_type, count in situational_errors.items():
            if count > 0:
                issues.append({
                    "topic": error_type,
                    "severity": count * self.weights["SITUATIONAL_ERROR"],
                    "context": f"Falló en adaptar sus objetos contra amenazas ({error_type.replace('_missed', '')}) en {count} partidas."
                })
        return issues

    def _evaluate_objective_deaths(self, summary_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evalúa y penaliza las muertes ocurridas justo antes de un objetivo neutral clave.
        """
        issues = []
        obj_deaths = summary_data.get("totals", {}).get("deaths_before_objectives", 0)
        if obj_deaths > 0:
            issues.append({
                "topic": "deaths_before_objectives",
                "severity": obj_deaths * self.weights["DEATH_BEFORE_OBJ"],
                "context": f"Murió {obj_deaths} veces justo antes de la aparición de un objetivo neutral clave."
            })
        return issues

    def _calculateRoleModifier(self, summaryData: Dict[str, Any], role: str, metric: str) -> float:
        # Calcula el multiplicador promedio para un rol basándose en los campeones jugados,
        # lo que permite tolerancias según el arquetipo (ej. Split-pushers pueden tener menos KP).
        recentMatches = summaryData.get("recent_matches", [])
        roleMatches = [m for m in recentMatches if m.get("role") == role]
        
        if not roleMatches:
            return 1.0
            
        totalModifier = 0.0
        for match in roleMatches:
            champion = match.get("champion", "")
            archetype = self.archetype_service.getArchetype(champion)
            totalModifier += self.archetype_service.getModifier(archetype, metric)
            
        return totalModifier / len(roleMatches)

    def _evaluate_benchmarks(self, summary_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Compara las métricas del jugador contra los estándares por rol y aplica modificadores de arquetipo.
        issues = []
        evaluations = summary_data.get("role_evaluations", {})
        
        for role, data in evaluations.items():
            evals = data.get("evaluation", {})
            role_key = role.upper() if role else "UNKNOWN"
            base_weights = self.role_weights.get(role_key, self.role_weights["UNKNOWN"])
            
            # Aplicamos los multiplicadores calculados a los pesos base
            cs_weight = base_weights.get("cs_per_min", 0) * self._calculateRoleModifier(summary_data, role, "cs_per_min")
            vision_weight = base_weights.get("vision_per_min", 0) * self._calculateRoleModifier(summary_data, role, "vision_per_min")
            kp_weight = base_weights.get("kill_participation", 0) * self._calculateRoleModifier(summary_data, role, "kill_participation")
            
            if evals.get("cs_per_min", {}).get("verdict") == "BELOW_STANDARD":
                issues.append({
                    "topic": f"low_cs_{role}",
                    "severity": cs_weight,
                    "context": f"Su farmeo (CS/min) jugando como {role} está por debajo de lo esperado."
                })
                
            if evals.get("vision_per_min", {}).get("verdict") == "BELOW_STANDARD":
                issues.append({
                    "topic": f"low_vision_{role}",
                    "severity": vision_weight,
                    "context": f"Su puntuación de visión por minuto jugando como {role} es deficiente y deja al equipo ciego."
                })
                
            if evals.get("kill_participation", {}).get("verdict") == "BELOW_STANDARD":
                issues.append({
                    "topic": f"low_kp_{role}",
                    "severity": kp_weight,
                    "context": f"Su participación en asesinatos jugando como {role} es baja, indicando falta de impacto en peleas."
                })
        return issues

    def _evaluate_lane_jungle_issues(self, summary_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evalúa deficiencias severas en la fase de líneas (déficit de súbditos)
        o en el rol de jungla (falta de aseguramiento de cangrejos).
        """
        issues = []
        recent_matches = summary_data.get("recent_matches", [])
        
        if not recent_matches:
            return issues

        cs_diff = recent_matches[0].get("max_cs_advantage_on_lane_opponent", 0)
        if cs_diff < -20:
            issues.append({
                "topic": "hard_lost_lane",
                "severity": 30,
                "context": f"Perdió la fase de líneas drásticamente, quedando {abs(cs_diff)} súbditos por detrás de su oponente directo."
            })
            
        is_jungle = summary_data.get("role_evaluations", {}).get("JUNGLE", {}).get("matches_played", 0) > 0
        if is_jungle:
            scuttles = recent_matches[0].get("scuttle_crab_kills", 1)
            if scuttles == 0:
                issues.append({
                    "topic": "no_scuttles",
                    "severity": 35,
                    "context": "Falló completamente en asegurar cangrejos del río, perdiendo visión crítica temprana."
                })
        
        return issues

    def evaluate_player_issues(self, summary_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analiza el resumen de datos del jugador, consolida todos los problemas detectados,
        los filtra y retorna los 3 más severos para enfocar el entrenamiento.
        """
        issues = []
        
        issues.extend(self._evaluate_situational_errors(summary_data))
        issues.extend(self._evaluate_objective_deaths(summary_data))
        issues.extend(self._evaluate_benchmarks(summary_data))
        issues.extend(self._evaluate_lane_jungle_issues(summary_data))

        # Filtrar incidencias sin severidad y ordenar de mayor a menor
        issues = [i for i in issues if i["severity"] > 0]
        issues.sort(key=lambda x: x["severity"], reverse=True)
        
        return issues[:3]
