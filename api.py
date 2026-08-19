import httpx
from config import settings
from fastapi import status, HTTPException


BASE_URL='https://api.football-data.org/v4/'
headers = {
        "X-Auth-Token": settings.API_FOOTBALL
    }


async def get_matches():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{BASE_URL}competitions/PL/matches', headers=headers)
            if response.status_code == 404:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException (status_code=502, detail=f'HTTPStatusError {str(e)}')
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f'Bad gateway {str(e)}')


async def get_standings():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{BASE_URL}competitions/PL/standings', headers=headers)
            if response.status_code == 404:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException (status_code=502, detail=f'HTTPStatusError {str(e)}')
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f'Bad gateway {str(e)}')

