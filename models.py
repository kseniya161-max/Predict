
from sqlalchemy import String, DateTime, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Match(Base):
    __tablename__='matches'
    id:Mapped[int] = mapped_column(primary_key=True)
    home_team:Mapped[str] = mapped_column(String(100))
    away_team:Mapped[str] = mapped_column(String(100))
    match_date:Mapped[DateTime] = mapped_column(DateTime)
    status:Mapped[str] = mapped_column(String(30))
    competition:Mapped[str] = mapped_column(String(100))


class Statistic(Base):
    __tablename__ = 'statistic'
    id: Mapped[int] = mapped_column(primary_key=True)
    team: Mapped[str] = mapped_column(String(100))
    wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    draws: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    losses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals_scored: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals_conceded: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

#
#
# id
# team
# title
# description
# published_at
# source
# url