from sqlalchemy import Column, Integer, BigInteger

from utils.db_api.base import Base


class Admins(Base):
    __tablename__ = 'admins'

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(BigInteger(), unique=True)