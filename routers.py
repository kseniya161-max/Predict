from http.client import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from sqlalchemy import select
from database import AsyncSessionLocal
from models import Statistic, Match, News, Prediction
from services import save_matches, save_statistics, save_news, calculate_prediction

router = APIRouter(prefix="/matches", tags=["matches"])
templates = Jinja2Templates(directory="templates")



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





@router.post("/news")
async def update_news():
    await save_news()
    return {"message": "News saved successfully"}


@router.get("/news")
async def news():
    async with AsyncSessionLocal() as session:
        result = await session.scalars(
            select(News)
        )
        return result.all()


@router.post("/matches/{match_id:int}")
async def get_predictions(match_id:int):
    result = await calculate_prediction(match_id)
    if not result:
        raise HTTPException(status_code=404, detail='Statistic or Match not found')
    return result


@router.get("/predictions")
async def get_predictions():
    async with AsyncSessionLocal() as session:
        result = await session.scalars(
            select(Prediction)
        )
        return result.all()



@router.get("/page")
async def matches_page(request: Request):
    async with AsyncSessionLocal() as session:
        result = await session.scalars(
            select(Match).order_by(Match.match_date)
        )
        matches = result.all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "matches": matches,
        },
    )

