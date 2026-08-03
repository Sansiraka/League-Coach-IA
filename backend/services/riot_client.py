import httpx
import asyncio
from typing import Dict, Any, List
from core.config import settings
from fastapi import HTTPException
import urllib.parse

class RiotClient:
    def __init__(self):
        self.headers = {
            "X-Riot-Token": settings.RIOT_API_KEY
        }
        self.base_url = "https://americas.api.riotgames.com"

    async def _request(self, endpoint: str) -> Any:
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            for attempt in range(3):
                response = await client.get(url, headers=self.headers)
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 2))
                    await asyncio.sleep(retry_after)
                    continue
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code, 
                        detail=f"Riot API Error: {response.text}"
                    )
                return response.json()
            raise HTTPException(status_code=429, detail="Rate limit exceeded after retries")

    async def get_account_by_riot_id(self, game_name: str, tag_line: str) -> Dict[str, Any]:
        game_name_enc = urllib.parse.quote(game_name)
        tag_line_enc = urllib.parse.quote(tag_line)
        return await self._request(f"/riot/account/v1/accounts/by-riot-id/{game_name_enc}/{tag_line_enc}")

    async def get_match_ids(self, puuid: str, queue: int = 440, count: int = 20) -> List[str]:
        return await self._request(f"/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={queue}&start=0&count={count}")

    async def get_match_details(self, match_id: str) -> Dict[str, Any]:
        return await self._request(f"/lol/match/v5/matches/{match_id}")

    async def get_match_timeline(self, match_id: str) -> Dict[str, Any]:
        return await self._request(f"/lol/match/v5/matches/{match_id}/timeline")
