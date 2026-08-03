from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi import HTTPException
from models.player import Player
from models.match import Match
from services.riot_client import RiotClient
from datetime import datetime

class SyncService:
    def __init__(self, db: Session):
        self.db = db
        self.riot_client = RiotClient()

    async def sync_player_matches(self, game_name: str, tag_line: str):
        # 1. Obtener PUUID desde Riot
        account_data = await self.riot_client.get_account_by_riot_id(game_name, tag_line)
        puuid = account_data["puuid"]

        # 2. Buscar o crear jugador localmente
        player = self.db.query(Player).filter(Player.puuid == puuid).first()
        if not player:
            player = Player(
                puuid=puuid,
                riot_id=account_data["gameName"],
                tag_line=account_data["tagLine"],
                region="americas"
            )
            self.db.add(player)
            self.db.commit()
            self.db.refresh(player)

        # 3. Obtener últimos matches de Flex
        match_ids = await self.riot_client.get_match_ids(puuid, queue=player.preferred_queue)
        
        saved_matches = 0
        for match_id in match_ids:
            # Verificar si ya existe en la base de datos local
            existing_match = self.db.query(Match).filter(Match.match_id == match_id).first()
            if existing_match:
                continue

            # Descargar detalle y timeline
            try:
                match_details = await self.riot_client.get_match_details(match_id)
                match_timeline = await self.riot_client.get_match_timeline(match_id)
                
                # Extraer info básica
                info = match_details.get("info", {})
                game_creation = info.get("gameCreation")
                if game_creation:
                    game_creation_dt = datetime.fromtimestamp(game_creation / 1000.0)
                else:
                    game_creation_dt = datetime.now()

                new_match = Match(
                    match_id=match_id,
                    game_creation=game_creation_dt,
                    game_duration=info.get("gameDuration"),
                    queue_id=info.get("queueId"),
                    patch=info.get("gameVersion"),
                    raw_match_json=match_details,
                    raw_timeline_json=match_timeline
                )
                self.db.add(new_match)
                saved_matches += 1
            except Exception as e:
                print(f"Error sincronizando {match_id}: {str(e)}")
                continue

        self.db.commit()
        return {"player": account_data["gameName"], "puuid": puuid, "saved_new_matches": saved_matches}
