from fastapi import APIRouter

from services import save_matches

router = APIRouter(prefix="/matches", tags=["matches"])


@router.post("/load")
async def load_matches():
    await save_matches()
    return {"messages": "matches are loaded successfully"}
