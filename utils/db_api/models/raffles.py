from sqlalchemy import Column, String, Integer, BigInteger

from utils.db_api.base import Base


class Raffles(Base):
    __tablename__ = 'raffles'

    id = Column(Integer(), primary_key=True)
    creator_id = Column(BigInteger(), unique=True)
    date = Column(String())
    amount = Column(String(), default='0')
    prize = Column(String())