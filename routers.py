from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, HTTPException
from sqlalchemy import select
from database import AsyncSessionLocal
from models import Statistic, Match, News, Prediction
from services import (
    save_matches,
    save_statistics,
    save_news,
    calculate_prediction,
    update_results,
)

router = APIRouter(prefix="/matches", tags=["matches"])
templates = Jinja2Templates(directory="templates")


@router.post("/load")
async def load_matches():
    await save_matches()
    return {"messages": "matches are loaded successfully"}


@router.post("/update-results")
async def update_match_results():
    await update_results()
    return {"message": "Results updated successfully"}


@router.post("/statistics")
async def update_statistics():
    await save_statistics()
    return {"message": "Statistics saved successfully"}


@router.get("/statistics")
async def get_statistics():
    async with AsyncSessionLocal() as session:
        result = await session.scalars(select(Statistic))

        return result.all()


@router.get("/matches")
async def get_matches():
    async with AsyncSessionLocal() as session:
        result = await session.scalars(select(Match))

        return result.all()


@router.post("/news")
async def update_news():
    await save_news()
    return {"message": "News saved successfully"}


@router.get("/news")
async def news():
    async with AsyncSessionLocal() as session:
        result = await session.scalars(select(News))
        return result.all()


@router.post("/matches/{match_id:int}")
async def get_predictions(match_id: int):
    result = await calculate_prediction(match_id)
    if not result:
        raise HTTPException(status_code=404, detail="Statistic or Match not found")
    return result


@router.get("/page")
async def matches_page(request: Request):
    async with AsyncSessionLocal() as session:
        result = await session.scalars(
            select(Match).order_by(Match.match_date).limit(10)
        )
        matches = result.all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "matches": matches,
        },
    )


@router.get("/{match_id}/prediction")
async def prediction_page(
    request: Request,
    match_id: int,
):
    async with AsyncSessionLocal() as session:
        match = await session.scalar(select(Match).where(Match.id == match_id))

        prediction = await session.scalar(
            select(Prediction)
            .where(Prediction.match_id == match_id)
            .order_by(Prediction.created_at.desc())
        )

    if not match or not prediction:
        raise HTTPException(status_code=404, detail="Match or prediction not found")

    return templates.TemplateResponse(
        request=request,
        name="prediction.html",
        context={
            "match": match,
            "prediction": prediction,
        },
    )


@router.get("/predictions")
async def get_predictions():
    async with AsyncSessionLocal() as session:
        result = await session.scalars(
            select(Prediction).order_by(Prediction.created_at.desc())
        )
        return result.all()


@router.get("/predictions/page")
async def predictions_page(request: Request):
    async with AsyncSessionLocal() as session:
        result = await session.scalars(
            select(Prediction).order_by(Prediction.created_at.desc())
        )
        predictions = result.all()

    return templates.TemplateResponse(
        request=request,
        name="predictions.html",
        context={
            "predictions": predictions,
        },
    )
