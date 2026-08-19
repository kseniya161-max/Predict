from fastapi import FastAPI
from database import engine
from routers import router


app = FastAPI()

app.include_router(router)
