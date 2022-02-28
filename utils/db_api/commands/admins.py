from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from utils.db_api.base import async_sessionmaker
from utils.db_api.models.admin import Admins


async def add_admin(telegram_id):
    try:
        async with async_sessionmaker() as session:
            await session.merge(Admins(telegram_id=telegram_id))
            await session.commit()
    except IntegrityError:
        return True


async def get_all_admins():
    async with async_sessionmaker() as session:
        counter = select(func.count('*')).select_from(Admins)
        result = await session.execute(counter)
        for row in result:
            return row[0]


async def get_admins():
    async with async_sessionmaker() as session:
        array = []
        info = select(Admins)
        result = await session.execute(info)

        for row in result.scalars():
            array.append(row.telegram_id)

        return array
