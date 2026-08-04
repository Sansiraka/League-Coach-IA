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

    def _format_recent_matches(self, recent_data: List[tuple], puuid: str) -> List[Dict[str, Any]]:
        """
        Formatea y extrae los datos de las partidas recientes incluyendo KDA y fecha extraídos del JSON crudo.
        """
        formatted = []
        for m, match_obj in recent_data:
            kills, deaths, assists = 0, 0, 0
            game_creation = match_obj.game_creation.isoformat() if match_obj.game_creation else None
            
            # Extraer KDA del raw_match_json
            if match_obj.raw_match_json and "info" in match_obj.raw_match_json:
                participants = match_obj.raw_match_json["info"].get("participants", [])
                p_data = next((p for p in participants if p.get("puuid") == puuid), None)
                if p_data:
                    kills = p_data.get("kills", 0)
                    deaths = p_data.get("deaths", 0)
                    assists = p_data.get("assists", 0)
            
            formatted.append({
                "match_id": m.match_id,
                "champion": m.champion,
                "role": m.role,
                "win": m.win,
                "game_creation": game_creation,
                "kills": kills,
                "deaths": deaths,
                "assists": assists,
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
            })
        return formatted

    def get_summary(self, game_name: str, tag_line: str, limit: int = 20) -> Dict[str, Any]:
        """
        Genera el resumen de analíticas del jugador, unificando métricas, benchmarks y prioridades de mejora.
        """
        player = self.db.query(Player).filter(Player.riot_id == game_name, Player.tag_line == tag_line).first()
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")

        self.process_unprocessed_matches(player)

        recent_data = self.db.query(PlayerMatchMetrics, Match)\
            .join(Match, PlayerMatchMetrics.match_id == Match.match_id)\
            .filter(PlayerMatchMetrics.player_id == player.id)\
            .order_by(desc(PlayerMatchMetrics.created_at))\
            .limit(limit)\
            .all()

        if not recent_data:
            return {"message": "No metrics available", "matches_analyzed": 0}
            
        recent_metrics = [m[0] for m in recent_data]

        count = len(recent_metrics)
        global_averages = self._calculate_global_averages(recent_metrics, count)
        situational_errors = self._calculate_situational_errors(recent_metrics)
        role_evaluations = self._evaluate_roles(recent_metrics)
        formatted_matches = self._format_recent_matches(recent_data, player.puuid)

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

    def get_match_details(self, match_id: str) -> Dict[str, Any]:
        """
        Extrae y formatea los detalles completos de una partida para el scoreboard (10 jugadores, equipos y objetivos).
        """
        match_obj = self.db.query(Match).filter(Match.match_id == match_id).first()
        if not match_obj or not match_obj.raw_match_json:
            raise HTTPException(status_code=404, detail="Match not found or raw data missing")

        info = match_obj.raw_match_json.get("info", {})
        
        teams_data = {}
        for team in info.get("teams", []):
            teams_data[team["teamId"]] = {
                "teamId": team["teamId"],
                "win": team.get("win", False),
                "objectives": team.get("objectives", {})
            }

        participants_data = []
        for p in info.get("participants", []):
            participants_data.append({
                "puuid": p.get("puuid"),
                "riotIdGameName": p.get("riotIdGameName") or p.get("summonerName", "Unknown"),
                "riotIdTagline": p.get("riotIdTagline", ""),
                "championName": p.get("championName"),
                "teamId": p.get("teamId"),
                "role": p.get("teamPosition") or p.get("role", "UNKNOWN"),
                "kills": p.get("kills", 0),
                "deaths": p.get("deaths", 0),
                "assists": p.get("assists", 0),
                "totalDamageDealtToChampions": p.get("totalDamageDealtToChampions", 0),
                "goldEarned": p.get("goldEarned", 0),
                "champLevel": p.get("champLevel", 0),
                "totalMinionsKilled": p.get("totalMinionsKilled", 0) + p.get("neutralMinionsKilled", 0),
                "visionScore": p.get("visionScore", 0),
                "dragonKills": p.get("dragonKills", 0),
                "baronKills": p.get("baronKills", 0),
                "turretKills": p.get("turretKills", 0),
                "inhibitorKills": p.get("inhibitorKills", 0),
                "items": [
                    p.get("item0", 0), p.get("item1", 0), p.get("item2", 0),
                    p.get("item3", 0), p.get("item4", 0), p.get("item5", 0), p.get("item6", 0)
                ]
            })

        return {
            "match_id": match_id,
            "game_creation": info.get("gameCreation"),
            "game_duration": info.get("gameDuration"),
            "teams": list(teams_data.values()),
            "participants": participants_data
        }
