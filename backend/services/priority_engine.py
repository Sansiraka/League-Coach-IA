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

    def _evaluate_highlight_strengths(self, summary_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evalúa y premia jugadas destacadas (highlights) y macroestrategia a lo largo de las partidas recientes.
        """
        strengths = []
        recent_matches = summary_data.get("recent_matches", [])
        
        if not recent_matches:
            return strengths
            
        lane_tyrant_score = 0
        macro_god_score = 0
        jungle_mastery_score = 0
        vision_control_score = 0
        
        # Outplays and mechanics
        total_saves = 0
        total_steals = 0
        total_outplays = 0
        total_dodges = 0

        for m in recent_matches:
            # 1. Lane Tyrant
            cs_adv = m.get("max_cs_advantage_on_lane_opponent", 0) or 0
            lvl_adv = m.get("max_level_lead_lane_opponent", 0) or 0
            lane_cs_10 = m.get("lane_minions_first_10_minutes", 0) or 0
            if cs_adv >= 20 or lvl_adv >= 2 or lane_cs_10 >= 75:
                lane_tyrant_score += 1
                
            # 2. Macro God
            plates = m.get("turret_plates", 0) or 0
            gold_15 = m.get("gold_diff_15", 0) or 0
            dives = m.get("kills_near_enemy_turret", 0) or 0
            if plates >= 3 or gold_15 >= 750 or dives >= 3:
                macro_god_score += 1
                
            # 3. Jungle Mastery
            if m.get("role") == "JUNGLE":
                epic_secure = m.get("epic_monster_kills_near_enemy_jungler", 0) or 0
                scuttles = m.get("scuttle_crab_kills", 0) or 0
                if epic_secure >= 1 or scuttles >= 2:
                    jungle_mastery_score += 1
                    
            # 4. Vision Control
            ward_takedowns = m.get("ward_takedowns_before_20m", 0) or 0
            if ward_takedowns >= 3:
                vision_control_score += 1
                
            # Acumular highlights mecánicos
            total_saves += m.get("save_ally_from_death", 0) or 0
            total_steals += m.get("epic_monster_steals", 0) or 0
            total_outplays += m.get("outnumbered_kills", 0) or 0
            total_dodges += m.get("skillshots_dodged", 0) or 0

        if lane_tyrant_score > 0:
            strengths.append({
                "topic": "lane_tyrant",
                "impact": lane_tyrant_score * 30, # Usando el peso absoluto de LANE_DOMINATED
                "context": f"Aplastaste tu línea (gran ventaja de farmeo o nivel) en {lane_tyrant_score} partidas recientes."
            })
            
        if macro_god_score > 0:
            strengths.append({
                "topic": "macro_god",
                "impact": macro_god_score * 25,
                "context": f"Demostraste excelente macrojuego (placas, asedios, ventaja de oro temprana) en {macro_god_score} partidas."
            })
            
        if jungle_mastery_score > 0:
            strengths.append({
                "topic": "jungle_mastery",
                "impact": jungle_mastery_score * 30, # Usando JUNGLE_DOMINATED
                "context": f"Aseguraste objetivos bajo presión y controlaste el río en {jungle_mastery_score} partidas como Jungla."
            })
            
        if vision_control_score > 0:
            strengths.append({
                "topic": "vision_control",
                "impact": vision_control_score * 25,
                "context": f"Denegaste visión enemiga de forma constante en juego temprano en {vision_control_score} partidas."
            })

        # Preservar los highlights mecánicos
        if total_saves > 0:
            strengths.append({
                "topic": "support_savior",
                "impact": total_saves * abs(self.weights.get("SUPPORT_SAVIOR", -25)),
                "context": f"Salvaste a aliados de una muerte segura en {total_saves} ocasiones."
            })
            
        if total_steals > 0:
            strengths.append({
                "topic": "epic_steals",
                "impact": total_steals * abs(self.weights.get("OUTPLAY", -15)) * 1.5,
                "context": f"Robaste {total_steals} monstruos épicos al equipo rival."
            })
            
        if total_outplays > 0:
            strengths.append({
                "topic": "outplays",
                "impact": total_outplays * abs(self.weights.get("OUTPLAY", -15)),
                "context": f"Lograste {total_outplays} asesinatos en inferioridad numérica."
            })

        if total_dodges > 10:
            strengths.append({
                "topic": "mechanical_god",
                "impact": (total_dodges // 10) * abs(self.weights.get("MECHANICAL_GOD", -20)), # Dividimos por 10 para balancear si el jugador esquiva miles
                "context": f"Esquivaste {total_dodges} habilidades clave, mostrando grandes mecánicas."
            })

        return strengths

    def _evaluate_benchmark_strengths(self, summary_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evalúa y premia métricas de rol que hayan superado el estándar.
        """
        strengths = []
        evaluations = summary_data.get("role_evaluations", {})
        
        for role, data in evaluations.items():
            evals = data.get("evaluation", {})
            role_key = role.upper() if role else "UNKNOWN"
            base_weights = self.role_weights.get(role_key, self.role_weights["UNKNOWN"])
            
            cs_weight = base_weights.get("cs_per_min", 0) * self._calculateRoleModifier(summary_data, role, "cs_per_min")
            vision_weight = base_weights.get("vision_per_min", 0) * self._calculateRoleModifier(summary_data, role, "vision_per_min")
            kp_weight = base_weights.get("kill_participation", 0) * self._calculateRoleModifier(summary_data, role, "kill_participation")
            
            if evals.get("cs_per_min", {}).get("verdict") == "ABOVE_STANDARD":
                strengths.append({
                    "topic": f"high_cs_{role}",
                    "impact": cs_weight * 1.5,
                    "context": f"Tu farmeo (CS/min) jugando como {role} está por encima del estándar esperado."
                })
                
            if evals.get("vision_per_min", {}).get("verdict") == "ABOVE_STANDARD":
                strengths.append({
                    "topic": f"high_vision_{role}",
                    "impact": vision_weight * 1.5,
                    "context": f"Lograste un excelente control de visión aportando al equipo jugando como {role}."
                })
                
            if evals.get("kill_participation", {}).get("verdict") == "ABOVE_STANDARD":
                strengths.append({
                    "topic": f"high_kp_{role}",
                    "impact": kp_weight * 1.5,
                    "context": f"Tuviste un alto impacto en peleas y rotaciones (Kill Participation) jugando como {role}."
                })
        return strengths

    def evaluate_player_strengths(self, summary_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analiza el resumen de datos del jugador, consolida logros y fortalezas destacadas,
        y retorna el Top 3 para alimentar el feedback positivo del LLM.
        """
        strengths = []
        
        strengths.extend(self._evaluate_highlight_strengths(summary_data))
        strengths.extend(self._evaluate_benchmark_strengths(summary_data))
        
        strengths = [s for s in strengths if s["impact"] > 0]
        strengths.sort(key=lambda x: x["impact"], reverse=True)
        
        return strengths[:3]
