# id
# home_team
# away_team
# match_date
# status
# competition
from sqlalchemy import String, DateTime
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




# team
# wins
# draws
# losses
# goals_scored
# goals_conceded
#
#
# id
# team
# title
# description
# published_at
# source
# url