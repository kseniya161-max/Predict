from fastapi import APIRouter
from sqlalchemy import select

from api import get_news
from database import AsyncSessionLocal
from models import Statistic, Match
from services import save_matches, save_statistics, save_news

router = APIRouter(prefix="/matches", tags=["matches"])



@router.post("/load")
async def load_matches():
    await save_matches()
    return {"messages": "matches are loaded successfully"}


@router.post("/statistics")
async def update_statistics():
    await save_statistics()
    return {"message": "Statistics saved successfully"}


@router.get("/statistics")
async def get_statistics():
    async with AsyncSessionLocal() as session:
        result = await session.scalars(
            select(Statistic)
        )

        return result.all()


@router.get("/matches")
async def get_matches():
    async with AsyncSessionLocal() as session:
        result = await session.scalars(
            select(Match)
        )

        return result.all()


@router.get("/news")
async def news():
    return await get_news()


@router.post("/news")
async def update_news():
    await save_news()
    return {"message": "News saved successfully"}
