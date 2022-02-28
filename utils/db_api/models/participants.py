from sqlalchemy import Integer, Column, BigInteger, String

from utils.db_api.base import Base


class Participants(Base):
    __tablename__ = 'participants'

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(BigInteger(), unique=True)
    username = Column(String())
