from typing import Dict

class ChampionArchetypeService:
    def __init__(self):
        # Mapea campeones conocidos a un arquetipo específico para poder ajustar
        # dinámicamente las expectativas de sus métricas.
        self.champion_to_archetype = {
            "Shen": "TANK_UTILITY",
            "Tryndamere": "SPLIT_PUSHER",
            "Zed": "ASSASSIN",
            "Ahri": "MAGE",
            "Jinx": "MARKSMAN",
            "Darius": "BRUISER",
            "Talon": "ASSASSIN",
            "Fiora": "SPLIT_PUSHER",
            "Braum": "TANK_UTILITY"
        }
        
        # Define los multiplicadores relativos por arquetipo.
        # Si un campeón es TANK_UTILITY, se espera menos farm (0.6) y más peleas (1.3).
        self.archetype_modifiers = {
            "TANK_UTILITY": {
                "cs_per_min": 0.6,
                "kill_participation": 1.3
            },
            "SPLIT_PUSHER": {
                "cs_per_min": 1.2,
                "kill_participation": 0.7
            },
            "ASSASSIN": {
                "vision_per_min": 1.2,
                "kill_participation": 1.2
            }
        }

    def getArchetype(self, championName: str) -> str:
        # Retorna el arquetipo asignado al campeón, o STANDARD si no está mapeado,
        # asegurando que el sistema no falle con campeones nuevos o desconocidos.
        return self.champion_to_archetype.get(championName, "STANDARD")

    def getModifier(self, archetype: str, metricName: str) -> float:
        # Retorna el multiplicador de la métrica. Si no existe un modificador específico,
        # retorna 1.0 (sin impacto) manteniendo la retrocompatibilidad.
        modifiers = self.archetype_modifiers.get(archetype, {})
        return modifiers.get(metricName, 1.0)
