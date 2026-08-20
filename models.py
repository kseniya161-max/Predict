from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger, Integer, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Match(Base):
    __tablename__ = "matches"
    id: Mapped[int] = mapped_column(primary_key=True)
    home_team: Mapped[str] = mapped_column(String(100))
    away_team: Mapped[str] = mapped_column(String(100))
    match_date: Mapped[DateTime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(30))
    competition: Mapped[str] = mapped_column(String(100))


class Statistic(Base):
    """ "турнирная статистика команд"""

    __tablename__ = "statistic"
    id: Mapped[int] = mapped_column(primary_key=True)
    team: Mapped[str] = mapped_column(String(100))
    wins: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    draws: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    losses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals_scored: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    goals_conceded: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class News(Base):
    __tablename__ = "news"
    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str | None]
    title: Mapped[str | None]
    description: Mapped[str | None]
    url: Mapped[str] = mapped_column(unique=True)
    image_url: Mapped[str | None]
    published_at: Mapped[datetime]
    content: Mapped[str | None]


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)

    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"),
        unique=True,
        nullable=False,
    )

    predicted_result: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    risk: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    score_home: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    score_away: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    reasons: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    actual_result: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    is_correct: Mapped[bool | None] = mapped_column(
        nullable=True,
    )
