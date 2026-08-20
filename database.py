import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv


from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
