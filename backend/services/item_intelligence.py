import json
import os
from typing import Dict, Any
from services.champion_archetype_service import ChampionArchetypeService

class ItemIntelligenceService:
    def __init__(self):
        self.archetype_service = ChampionArchetypeService()
        config_path = os.path.join(os.path.dirname(__file__), "..", "data", "items_config.json")
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading items config: {e}")
            self.config = {}

    def _hasTeamPurchasedItem(self, allies: list, targetItems: list) -> bool:
        # Verifica si al menos un aliado ha comprado alguno de los objetos clave,
        # para evitar penalizar al jugador si la necesidad ya está cubierta grupalmente.
        target_set = set(targetItems)
        for ally in allies:
            for i in range(7):
                if ally.get(f"item{i}", 0) in target_set:
                    return True
        return False

    def analyze(self, match: Any, player_puuid: str, player_role: str = None) -> Dict[str, Any]:
        """
        Analiza las decisiones de objetos del jugador en base a la composición enemiga.
        """
        match_data = match.raw_match_json
        if not match_data or "info" not in match_data:
            return {}

        participants = match_data["info"]["participants"]
        
        # Encontrar al jugador y su equipo
        player_p = None
        for p in participants:
            if p.get("puuid") == player_puuid:
                player_p = p
                break
                
        if not player_p:
            return {}

        player_team_id = player_p.get("teamId")
        champion_name = player_p.get("championName", "")
        archetype = self.archetype_service.getArchetype(champion_name)
        
        # Separar aliados y enemigos
        enemies = [p for p in participants if p.get("teamId") != player_team_id]
        allies = [p for p in participants if p.get("teamId") == player_team_id and p.get("participantId") != player_p.get("participantId")]
        
        # Extraer objetos del jugador
        player_items = set()
        for i in range(7):
            item_id = player_p.get(f"item{i}", 0)
            if item_id > 0:
                player_items.add(item_id)

        results = {}

        # 1. Regla: Amenaza de Curación (Anti-Heal)
        if "grievous_wounds" in self.config:
            gw_config = self.config["grievous_wounds"]
            total_healing = sum(e.get("totalHeal", 0) + e.get("totalHealsOnTeammates", 0) for e in enemies)
            threat = total_healing > gw_config["threshold_healing"]
            
            purchased = bool(player_items.intersection(set(gw_config["items"])))
            team_covered = self._hasTeamPurchasedItem(allies, gw_config["items"])
            
            verdict = "NOT_NEEDED"
            if threat and purchased:
                verdict = "CORRECT"
            elif threat and not purchased and team_covered:
                # El equipo ya tiene corta curas, el jugador no está obligado a comprarlo.
                verdict = "TEAM_COVERED"
            elif threat and not purchased:
                verdict = "MISSED"
                
            results["anti_heal"] = {
                "threat": threat,
                "threat_value": total_healing,
                "purchased": purchased,
                "verdict": verdict
            }

        # 2. Regla: Daño Mágico (Resistencia Mágica)
        if "magic_resistance" in self.config:
            mr_config = self.config["magic_resistance"]
            total_magic_dmg = sum(e.get("magicDamageDealtToChampions", 0) for e in enemies)
            total_dmg = sum(e.get("totalDamageDealtToChampions", 0) for e in enemies)
            
            magic_pct = (total_magic_dmg / total_dmg * 100) if total_dmg > 0 else 0
            threat = magic_pct > mr_config["threshold_magic_damage_pct"]
            
            purchased = bool(player_items.intersection(set(mr_config["items"])))
            
            verdict = "NOT_NEEDED"
            # Si el jugador es un rol muy frágil que no suele armar resistencias puras, lo eximimos.
            if archetype in ["MAGE", "MARKSMAN", "ASSASSIN"]:
                verdict = "EXEMPT"
            elif threat and not purchased:
                verdict = "MISSED"
            elif threat and purchased:
                verdict = "CORRECT"
                
            results["anti_ap"] = {
                "threat": threat,
                "threat_value_pct": round(magic_pct, 2),
                "purchased": purchased,
                "verdict": verdict
            }

        # 3. Regla: Control de Masas (Tenacidad)
        if "tenacity" in self.config:
            tenacity_config = self.config["tenacity"]
            total_cc_time = sum(e.get("timeCCingOthers", 0) for e in enemies)
            threat = total_cc_time > tenacity_config["threshold_cc_time_s"]
            
            purchased = bool(player_items.intersection(set(tenacity_config["items"])))
            # 3222 = Crisol de Mikael (Mikael's Blessing), el principal objeto de soporte anti-CC.
            team_covered = self._hasTeamPurchasedItem(allies, [3222])
            is_adc = (player_role == "BOTTOM" or archetype == "MARKSMAN")
            
            verdict = "NOT_NEEDED"
            if threat and purchased:
                verdict = "CORRECT"
            elif threat and not purchased and team_covered and is_adc:
                # Un soporte o aliado compró Mikael exclusivamente para salvar al tirador.
                verdict = "TEAM_COVERED"
            elif threat and not purchased:
                verdict = "MISSED"
                
            results["anti_cc"] = {
                "threat": threat,
                "threat_value": total_cc_time,
                "purchased": purchased,
                "verdict": verdict
            }

        # 4. Regla: Anti-AD (Armadura)
        if "armor" in self.config:
            armor_conf = self.config["armor"]
            t_phys = sum(e.get("physicalDamageDealtToChampions", 0) for e in enemies)
            t_dmg = sum(e.get("totalDamageDealtToChampions", 0) for e in enemies)
            phys_pct = (t_phys / t_dmg) if t_dmg > 0 else 0
            threat = phys_pct > 0.65
            purchased = bool(player_items.intersection(set(armor_conf)))
            
            verdict = "NOT_NEEDED"
            if archetype in ["MAGE", "MARKSMAN", "ASSASSIN"]:
                verdict = "EXEMPT"
            elif threat and not purchased:
                verdict = "MISSED"
            elif threat and purchased:
                verdict = "CORRECT"

            results["anti_ad"] = {
                "threat": threat,
                "threat_value_pct": round(phys_pct * 100, 2),
                "purchased": purchased,
                "verdict": verdict
            }

        # 5. Regla: Anti-Burst
        if "anti_burst" in self.config:
            burst_conf = self.config["anti_burst"]
            fed_enemy = next((e for e in enemies if e.get("challenges", {}).get("teamDamagePercentage", 0) > 0.40), None)
            threat = fed_enemy is not None
            purchased = bool(player_items.intersection(set(burst_conf)))
            
            verdict = "NOT_NEEDED"
            if archetype in ["MARKSMAN"]: # Magos y asesinos sí pueden usar Zhonyas/Edge of Night
                verdict = "EXEMPT"
            elif threat and not purchased:
                verdict = "MISSED"
            elif threat and purchased:
                verdict = "CORRECT"

            res = {
                "threat": threat,
                "purchased": purchased,
                "verdict": verdict
            }
            if fed_enemy:
                res["fed_champion"] = fed_enemy.get("championName", "Unknown")
            results["anti_burst"] = res

        # 6. Regla: Anti-Split Push
        if player_role == "TOP":
            split_enemy = next((e for e in enemies if e.get("damageDealtToTurrets", 0) > 6000), None)
            threat = split_enemy is not None
            has_tp = player_p.get("summoner1Id") == 12 or player_p.get("summoner2Id") == 12
            has_hull = 3181 in player_items # Hullbreaker item ID
            purchased = has_tp or has_hull
            results["anti_split"] = {
                "threat": threat,
                "purchased": purchased,
                "verdict": "CORRECT" if threat and purchased else "MISSED" if threat else "NOT_NEEDED"
            }

        return results
