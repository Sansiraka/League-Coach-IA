from typing import Dict, Any
from models.match import Match
from models.player import Player
from services.item_intelligence import ItemIntelligenceService

class MetricsEngine:
    """
    Motor de cálculo de métricas de jugador.
    Se encarga de procesar los datos crudos de la partida y de la línea de tiempo
    para extraer estadísticas relevantes de rendimiento.
    """
    def __init__(self):
        self.item_intelligence = ItemIntelligenceService()

    def _get_death_threshold_ms(self, objective_timestamp_ms: int) -> int:
        """
        Devuelve el umbral en milisegundos según el momento de la partida:
        - < 15 min (900000 ms): 30s (30000 ms)
        - < 30 min (1800000 ms): 40s (40000 ms)
        - >= 30 min (1800000 ms): 70s (70000 ms)
        """
        if objective_timestamp_ms < 900000:
            return 30000
        elif objective_timestamp_ms < 1800000:
            return 40000
        else:
            return 70000

    def _detect_support_cs_steal(self, frames: list, support_id: int, team_id: int, participants: list) -> str:
        """
        Detecta si el support está robando farm al ADC aliado comparando CS al min 10 y 15.
        """
        adc_participant = next((p for p in participants if p.get("teamId") == team_id and p.get("teamPosition") == "BOTTOM"), None)
        if not adc_participant:
            return "OK"
        
        adc_id = adc_participant.get("participantId")
        support_cs_15 = 0
        adc_cs_15 = 0
        
        for frame in frames:
            timestamp = frame.get("timestamp", 0)
            if 890000 <= timestamp <= 910000:
                support_frame = frame.get("participantFrames", {}).get(str(support_id), {})
                adc_frame = frame.get("participantFrames", {}).get(str(adc_id), {})
                support_cs_15 = support_frame.get("minionsKilled", 0)
                adc_cs_15 = adc_frame.get("minionsKilled", 0)
                break
                
        if support_cs_15 <= 25:
            return "OK"
        elif support_cs_15 > 25 and adc_cs_15 < 100:
            return "STEALING_CS"
        else:
            return "FARMING_SOLO"

    def _extract_basic_stats(self, player_participant: Dict[str, Any], team_kills: int, game_duration_min: float) -> Dict[str, Any]:
        """
        Extrae y calcula las métricas básicas de rendimiento del jugador (farmeo, oro, visión, y KDA).
        """
        total_cs = player_participant.get("totalMinionsKilled", 0) + player_participant.get("neutralMinionsKilled", 0)
        kills = player_participant.get("kills", 0)
        assists = player_participant.get("assists", 0)
        
        return {
            "cs_per_min": round(total_cs / game_duration_min, 2) if game_duration_min > 0 else 0,
            "gold_per_min": round(player_participant.get("goldEarned", 0) / game_duration_min, 2) if game_duration_min > 0 else 0,
            "vision_per_min": round(player_participant.get("visionScore", 0) / game_duration_min, 2) if game_duration_min > 0 else 0,
            "kill_participation": round((kills + assists) / team_kills, 2) if team_kills > 0 else 0.0
        }

    def _extract_advanced_stats(self, player_participant: Dict[str, Any], challenges: Dict[str, Any]) -> Dict[str, Any]:
        """
        Obtiene las estadísticas avanzadas provistas por la API de Riot (daño, escudos, control de masas, etc.).
        """
        return {
            "team_damage_percentage": round(challenges.get("teamDamagePercentage", 0.0) * 100, 2),
            "damage_mitigated": player_participant.get("damageSelfMitigated", 0),
            "heal_shield_effective": challenges.get("effectiveHealAndShielding", 0),
            "cc_time": player_participant.get("timeCCingOthers", 0),
            "turret_plates": challenges.get("turretPlatesTaken", 0)
        }

    def _calculate_vision_metrics(self, player_participant: Dict[str, Any], challenges: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recopila métricas detalladas relacionadas con el control de visión.
        """
        return {
            "wards_placed": player_participant.get("wardsPlaced", 0),
            "wards_killed": player_participant.get("wardsKilled", 0),
            "vision_wards_bought": player_participant.get("visionWardsBoughtInGame", 0),
            "vision_score_advantage": challenges.get("visionScoreAdvantageLaneOpponent", 0.0)
        }

    def _get_gold_at_minute(self, frame: Dict[str, Any], participant_id: int, opponent_id: int) -> float:
        """
        Obtiene la diferencia de oro entre el jugador y su oponente en un frame específico.
        """
        participant_frame = frame.get("participantFrames", {}).get(str(participant_id), {})
        player_gold = participant_frame.get("totalGold", 0)
        opp_gold = 0
        if opponent_id:
            opp_frame = frame.get("participantFrames", {}).get(str(opponent_id), {})
            opp_gold = opp_frame.get("totalGold", 0)
        return player_gold - opp_gold

    def _extract_timeline_data(self, timeline: Dict[str, Any], participant_id: int, opponent_id: int, team_position: str, team_id: int, participants: list) -> Dict[str, Any]:
        """
        Analiza la línea de tiempo de la partida para extraer diferencias de oro y detectar patrones específicos.
        """
        result = {
            "gold_diff_10": 0.0, "gold_diff_15": 0.0, "gold_diff_25": 0.0,
            "deaths_before_objectives": 0, "support_cs_alert": None
        }
        
        if not timeline or "info" not in timeline:
            return result

        frames = timeline["info"].get("frames", [])
        
        for frame in frames:
            timestamp = frame.get("timestamp", 0)
            if 590000 <= timestamp <= 610000:
                result["gold_diff_10"] = self._get_gold_at_minute(frame, participant_id, opponent_id)
            if 890000 <= timestamp <= 910000:
                result["gold_diff_15"] = self._get_gold_at_minute(frame, participant_id, opponent_id)
            if 1490000 <= timestamp <= 1510000:
                result["gold_diff_25"] = self._get_gold_at_minute(frame, participant_id, opponent_id)

        if team_position == "UTILITY":
            result["support_cs_alert"] = self._detect_support_cs_steal(frames, participant_id, team_id, participants)

        result["deaths_before_objectives"] = self._count_deaths_before_objectives(frames, participant_id)
        return result

    def _count_deaths_before_objectives(self, frames: list, participant_id: int) -> int:
        """
        Cuenta cuántas veces el jugador murió justo antes de que se capturara un objetivo élite.
        """
        player_deaths = []
        objective_kills = []
        
        for frame in frames:
            for event in frame.get("events", []):
                event_type = event.get("type")
                if event_type == "CHAMPION_KILL" and event.get("victimId") == participant_id:
                    player_deaths.append(event.get("timestamp"))
                elif event_type == "ELITE_MONSTER_KILL":
                    objective_kills.append(event.get("timestamp"))

        deaths = 0
        for obj_time in objective_kills:
            threshold = self._get_death_threshold_ms(obj_time)
            for death_time in player_deaths:
                if (obj_time - threshold) <= death_time < obj_time:
                    deaths += 1
                    break
        return deaths

    def calculate_metrics(self, match: Match, player: Player) -> Dict[str, Any]:
        """
        Calcula y agrupa todas las métricas del jugador para una partida específica.
        """
        info = match.raw_match_json.get("info", {})
        participants = info.get("participants", [])
        
        player_participant = next((p for p in participants if p.get("puuid") == player.puuid), None)
        if not player_participant:
            raise ValueError(f"Player {player.puuid} not found in match {match.match_id}")

        team_id = player_participant.get("teamId")
        participant_id = player_participant.get("participantId")
        team_position = player_participant.get("teamPosition", "UNKNOWN")
        
        opponent = next((p for p in participants if p.get("teamId") != team_id and p.get("teamPosition") == team_position), None)
        opponent_id = opponent.get("participantId") if opponent else None
        
        team_kills = sum(p.get("kills", 0) for p in participants if p.get("teamId") == team_id)
        game_duration_min = max(info.get("gameDuration", 0) / 60.0, 1.0)
        
        challenges = player_participant.get("challenges", {})
        
        basic_stats = self._extract_basic_stats(player_participant, team_kills, game_duration_min)
        advanced_stats = self._extract_advanced_stats(player_participant, challenges)
        vision_metrics = self._calculate_vision_metrics(player_participant, challenges)
        timeline_data = self._extract_timeline_data(
            match.raw_timeline_json, participant_id, opponent_id, team_position, team_id, participants
        )
        
        situational_analysis = self.item_intelligence.analyze(match, player.puuid, team_position)

        return {
            "match_id": match.match_id,
            "player_id": player.id,
            "champion": player_participant.get("championName"),
            "role": team_position,
            "win": player_participant.get("win", False),
            **basic_stats,
            **advanced_stats,
            **vision_metrics,
            **timeline_data,
            "situational_analysis_json": situational_analysis,
            "solo_kills": challenges.get("soloKills", 0),
            "lane_minions_first_10_minutes": challenges.get("laneMinionsFirst10Minutes", 0),
            "max_cs_advantage_on_lane_opponent": challenges.get("maxCsAdvantageOnLaneOpponent", 0.0),
            "max_level_lead_lane_opponent": challenges.get("maxLevelLeadLaneOpponent", 0),
            "jungle_cs_before_10_minutes": challenges.get("jungleCsBefore10Minutes", 0.0),
            "epic_monster_steals": challenges.get("epicMonsterSteals", 0),
            "scuttle_crab_kills": challenges.get("scuttleCrabKills", 0),
            "epic_monster_kills_near_enemy_jungler": challenges.get("epicMonsterKillsNearEnemyJungler", 0),
            "ward_takedowns_before_20m": challenges.get("wardTakedownsBefore20M", 0),
            "save_ally_from_death": challenges.get("saveAllyFromDeath", 0),
            "skillshots_dodged": challenges.get("skillshotsDodged", 0),
            "skillshots_hit": challenges.get("skillshotsHit", 0),
            "outnumbered_kills": challenges.get("outnumberedKills", 0),
            "kills_near_enemy_turret": challenges.get("killsNearEnemyTurret", 0)
        }
