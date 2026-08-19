from fastapi import APIRouter
from sqlalchemy import select

from database import AsyncSessionLocal
from models import Statistic
from services import save_matches, save_statistics

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
