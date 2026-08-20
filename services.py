from datetime import datetime
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api import get_matches, get_standings, get_news
from models import Match, Statistic, News, Prediction
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


async def save_statistics():
    data = await get_standings()
    table = data["standings"][0]["table"]

    async with AsyncSessionLocal() as session:
        for item in table:
            existing_item = await session.scalar(
                select(Statistic).where(
                    Statistic.team == item["team"]["name"]
                )
            )

            if existing_item:
                existing_item.wins = item["won"]
                existing_item.draws = item["draw"]
                existing_item.losses = item["lost"]
                existing_item.goals_scored = item["goalsFor"]
                existing_item.goals_conceded = item["goalsAgainst"]

            else:
                new_statistic = Statistic(
                    team=item["team"]["name"],
                    wins=item["won"],
                    draws=item["draw"],
                    losses=item["lost"],
                    goals_scored=item["goalsFor"],
                    goals_conceded=item["goalsAgainst"],
                )

                session.add(new_statistic)

        await session.commit()


async def save_news():
    data = await get_news()
    articles = data["articles"]
    async with AsyncSessionLocal() as session:
        for article in articles:
            existing_news = await session.scalar(select(News).where (News.url == article['url']))
            if existing_news:
                continue


            new_news = News(
                author=article["author"],
                title=article["title"],
                description=article["description"],
                url=article["url"],
                image_url=article["urlToImage"],
                published_at=datetime.fromisoformat(
                    article["publishedAt"].replace("Z", "+00:00")
                ),
                content=article["content"],
            )

            session.add(new_news)
        await session.commit()


async def calculate_prediction(match_id: int):
    async with AsyncSessionLocal() as session:
        match = await session.scalar(select(Match).where(Match.id == match_id))
        if not match:
            return None
        home_stat = await session.scalar(select(Statistic).where(Statistic.team == match.home_team))
        away_stat = await session.scalar(select(Statistic).where(Statistic.team == match.away_team))

        home_news = await session.scalars(select(News).where(News.title.ilike(f'%{match.home_team}%')))
        away_news = await session.scalars(select(News).where (News.title.ilike(f'%{match.away_team}%')))

        home_news = home_news.all()
        away_news = away_news.all()

        home_news_score = get_news_score(home_news)
        away_news_score = get_news_score(away_news)

        if not home_stat or not away_stat:
            raise HTTPException(status_code=404,detail='NOT FOUND')
        home_form = home_stat.wins * 3 + home_stat.draws
        away_form = away_stat.wins * 3 + away_stat.draws

        home_attack = home_stat.goals_scored
        away_attack = away_stat.goals_scored

        home_defense = -home_stat.goals_conceded
        away_defense = -away_stat.goals_conceded

        home_score = (
                home_form * 0.5
                + home_attack * 0.3
                + home_defense * 0.2
        )

        away_score = (
                away_form * 0.5
                + away_attack * 0.3
                + away_defense * 0.2
        )

        home_score += home_news_score
        away_score += away_news_score

        difference = abs(home_score - away_score)

        if difference < 5:
            predicted_result = "DRAW"
        elif home_score > away_score:
            predicted_result = "HOME_WIN"
        else:
            predicted_result = "AWAY_WIN"

        confidence = min(95, 50 + difference)
        if difference < 5:
            risk = "HIGH"
        elif difference < 15:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        reasons = [
            f"{match.home_team} score: {home_score:.2f}",
            f"{match.away_team} score: {away_score:.2f}",
            f"{match.home_team} news score: {home_news_score}",
            f"{match.away_team} news score: {away_news_score}",
            f"Score difference: {difference:.2f}",
        ]

        prediction = Prediction(
            match_id=match.id,
            predicted_result=predicted_result,
            confidence=confidence,
            risk=risk,
            score_home=home_score,
            score_away=away_score,
            reasons="\n".join(reasons),
        )

        session.add(prediction)
        await session.commit()

        return prediction


POSITIVE_WORDS = [
    "win", "victory", "return", "returns", "boost",
    "good", "positive", "success", "sign"
]

NEGATIVE_WORDS = [
    "injury", "injured", "loss", "lose", "suspension",
    "suspended", "out", "negative", "problem"
]

def get_news_score(news):
    score = 0
    for item in news:
        text = f"{item.title or ''} {item.description or ''}".lower()
        for word in POSITIVE_WORDS:
            if word in text:
                score += 1
        for word in NEGATIVE_WORDS:
            if word in text:
                score -= 1
    return score


async def update_results():
    data = await get_matches()

    async with AsyncSessionLocal() as session:
        for item in data["matches"]:
            match = await session.scalar(
                select(Match).where(Match.id == item["id"])
            )

            if not match:
                continue

            match.status = item["status"]


            if item["status"] != "FINISHED":
                continue

            score = item["score"]["fullTime"]

            home_score = score["home"]
            away_score = score["away"]

            if home_score > away_score:
                actual_result = "HOME_WIN"
            elif away_score > home_score:
                actual_result = "AWAY_WIN"
            else:
                actual_result = "DRAW"

            prediction = await session.scalar(
                select(Prediction).where(
                    Prediction.match_id == match.id
                )
            )

            if prediction:
                prediction.actual_result = actual_result
                prediction.is_correct = (
                    prediction.predicted_result == actual_result
                )

        await session.commit()


