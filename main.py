from fastapi import FastAPI,Request
from starlette.templating import Jinja2Templates

from database import engine
from routers import router


app = FastAPI()
app.include_router(router)


