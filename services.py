from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api import get_matches
from models import Match
from database import AsyncSessionLocal


async def save_matches():
    data = await get_matches()
    matches = data["matches"]

    async with AsyncSessionLocal() as session:
        for match in matches:
            existing_match = await session.scalar(
                select(Match).where(Match.id == match["id"])
            )

            if existing_match:
                continue

            new_match = Match(
                id=match["id"],
                home_team=match["homeTeam"]["name"],
                away_team=match["awayTeam"]["name"],
                match_date=datetime.fromisoformat(
                    match["utcDate"].replace("Z", "+00:00")
                ),
                status=match["status"],
                competition=match["competition"]["name"],
            )

            session.add(new_match)

        await session.commit()