from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from collections import defaultdict
from models.player import Player
from models.match import Match
from models.metrics import PlayerMatchMetrics
from services.metrics_engine import MetricsEngine
from services.benchmark_service import BenchmarkService
from services.priority_engine import PriorityEngine
from fastapi import HTTPException
from typing import List, Dict, Any

class AnalyticsService:
    """
    Servicio encargado de procesar y consolidar las métricas analíticas de los jugadores,
    generando resúmenes y benchmarks para facilitar el coaching.
    """
    def __init__(self, db: Session):
        self.db = db
        self.engine = MetricsEngine()
        self.benchmark_service = BenchmarkService()

    def process_unprocessed_matches(self, player: Player):
        """
        Calcula y guarda métricas para aquellas partidas del jugador que aún no han sido procesadas.
        """
        subquery = self.db.query(PlayerMatchMetrics.match_id).filter(PlayerMatchMetrics.player_id == player.id)
        
        unprocessed_matches = self.db.query(Match).filter(~Match.match_id.in_(subquery)).all()
        
        for match in unprocessed_matches:
            try:
                metrics_data = self.engine.calculate_metrics(match, player)
                new_metrics = PlayerMatchMetrics(**metrics_data)
                self.db.add(new_metrics)
            except Exception as e:
                print(f"Error procesando métricas para match {match.match_id}: {str(e)}")
                continue
                
        self.db.commit()

    def _calculate_global_averages(self, recent_metrics: List[PlayerMatchMetrics], count: int) -> Dict[str, Any]:
        """
        Calcula los promedios globales (KDA, CS, Visión) de las últimas partidas procesadas.
        """
        avg_cs = sum(m.cs_per_min for m in recent_metrics if m.cs_per_min) / count
        avg_kp = sum(m.kill_participation for m in recent_metrics if m.kill_participation) / count
        avg_vision = sum(m.vision_per_min for m in recent_metrics if m.vision_per_min) / count
        total_obj_deaths = sum(m.deaths_before_objectives for m in recent_metrics if m.deaths_before_objectives)
        win_rate = sum(1 for m in recent_metrics if m.win) / count

        return {
            "win_rate": round(win_rate * 100, 2),
            "averages": {
                "cs_per_min": round(avg_cs, 2),
                "kill_participation": round(avg_kp * 100, 2),
                "vision_per_min": round(avg_vision, 2)
            },
            "total_obj_deaths": total_obj_deaths
        }

    def _calculate_situational_errors(self, recent_metrics: List[PlayerMatchMetrics]) -> Dict[str, int]:
        """
        Agrega la cantidad de errores de itemización situacional detectados en las últimas partidas.
        """
        situational_errors = {
            "anti_heal_missed": 0, "anti_ap_missed": 0, "anti_cc_missed": 0,
            "anti_ad_missed": 0, "anti_burst_missed": 0, "anti_split_missed": 0
        }
        for m in recent_metrics:
            if m.situational_analysis_json:
                for key in situational_errors.keys():
                    base_key = key.replace("_missed", "")
                    if base_key in m.situational_analysis_json:
                        if m.situational_analysis_json[base_key].get("verdict") == "MISSED":
                            situational_errors[key] += 1
        return situational_errors

    def _evaluate_roles(self, recent_metrics: List[PlayerMatchMetrics]) -> Dict[str, Any]:
        """
        Agrupa las partidas por rol y compara las métricas contra los benchmarks esperados.
        """
        role_metrics = defaultdict(list)
        for m in recent_metrics:
            role = m.role or "UNKNOWN"
            role_metrics[role].append(m)

        role_evaluations = {}
        for role, metrics_list in role_metrics.items():
            r_count = len(metrics_list)
            
            def avg(field):
                return sum(getattr(m, field) for m in metrics_list if getattr(m, field)) / r_count

            metrics_to_evaluate = {
                "cs_per_min": round(avg("cs_per_min"), 2),
                "kill_participation": round(avg("kill_participation") * 100, 2),
                "vision_per_min": round(avg("vision_per_min"), 2),
                "gold_diff_15": round(avg("gold_diff_15"), 2),
                "team_damage_percentage": round(avg("team_damage_percentage"), 2),
                "damage_mitigated": round(avg("damage_mitigated"), 2),
                "heal_shield_effective": round(avg("heal_shield_effective"), 2),
                "cc_time": round(avg("cc_time"), 2),
                "turret_plates": round(avg("turret_plates"), 2),
                "gold_diff_25": round(avg("gold_diff_25"), 2),
                "wards_placed": round(avg("wards_placed"), 2),
                "wards_killed": round(avg("wards_killed"), 2),
                "vision_wards_bought": round(avg("vision_wards_bought"), 2),
                "vision_score_advantage": round(avg("vision_score_advantage"), 2)
            }
            
            evaluation = self.benchmark_service.evaluate_metrics(role, metrics_to_evaluate)
            role_evaluations[role] = {
                "matches_played": r_count,
                "evaluation": evaluation
            }

        return role_evaluations

    def _format_recent_matches(self, recent_metrics: List[PlayerMatchMetrics]) -> List[Dict[str, Any]]:
        """
        Formatea y extrae los datos de las partidas recientes para incluir en el resumen final.
        """
        return [
            {
                "match_id": m.match_id,
                "champion": m.champion,
                "role": m.role,
                "win": m.win,
                "deaths_before_objectives": m.deaths_before_objectives,
                "gold_diff_10": m.gold_diff_10,
                "gold_diff_15": m.gold_diff_15,
                "gold_diff_25": m.gold_diff_25,
                "team_damage_percentage": m.team_damage_percentage,
                "damage_mitigated": m.damage_mitigated,
                "heal_shield_effective": m.heal_shield_effective,
                "cc_time": m.cc_time,
                "turret_plates": m.turret_plates,
                "wards_placed": m.wards_placed,
                "wards_killed": m.wards_killed,
                "vision_wards_bought": m.vision_wards_bought,
                "vision_score_advantage": m.vision_score_advantage,
                "support_cs_alert": m.support_cs_alert,
                "situational_analysis_json": m.situational_analysis_json,
                "save_ally_from_death": m.save_ally_from_death,
                "epic_monster_steals": m.epic_monster_steals,
                "outnumbered_kills": m.outnumbered_kills,
                "skillshots_dodged": m.skillshots_dodged,
                "max_cs_advantage_on_lane_opponent": m.max_cs_advantage_on_lane_opponent,
                "lane_minions_first_10_minutes": m.lane_minions_first_10_minutes,
                "max_level_lead_lane_opponent": m.max_level_lead_lane_opponent,
                "kills_near_enemy_turret": m.kills_near_enemy_turret,
                "epic_monster_kills_near_enemy_jungler": m.epic_monster_kills_near_enemy_jungler,
                "scuttle_crab_kills": m.scuttle_crab_kills,
                "ward_takedowns_before_20m": m.ward_takedowns_before_20m
            } for m in recent_metrics
        ]

    def get_summary(self, game_name: str, tag_line: str, limit: int = 20) -> Dict[str, Any]:
        """
        Genera el resumen de analíticas del jugador, unificando métricas, benchmarks y prioridades de mejora.
        """
        player = self.db.query(Player).filter(Player.riot_id == game_name, Player.tag_line == tag_line).first()
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")

        self.process_unprocessed_matches(player)

        recent_metrics = self.db.query(PlayerMatchMetrics)\
            .filter(PlayerMatchMetrics.player_id == player.id)\
            .order_by(desc(PlayerMatchMetrics.created_at))\
            .limit(limit)\
            .all()

        if not recent_metrics:
            return {"message": "No metrics available", "matches_analyzed": 0}

        count = len(recent_metrics)
        global_averages = self._calculate_global_averages(recent_metrics, count)
        situational_errors = self._calculate_situational_errors(recent_metrics)
        role_evaluations = self._evaluate_roles(recent_metrics)
        formatted_matches = self._format_recent_matches(recent_metrics)

        summary_data = {
            "player": f"{game_name}#{tag_line}",
            "matches_analyzed": count,
            "win_rate": global_averages["win_rate"],
            "averages": global_averages["averages"],
            "role_evaluations": role_evaluations,
            "totals": {
                "deaths_before_objectives": global_averages["total_obj_deaths"],
                "situational_errors": situational_errors
            },
            "recent_matches": formatted_matches
        }
        
        priority_engine = PriorityEngine()
        summary_data["top_priorities"] = priority_engine.evaluate_player_issues(summary_data)
        summary_data["top_strengths"] = priority_engine.evaluate_player_strengths(summary_data)
        
        
        return summary_data
