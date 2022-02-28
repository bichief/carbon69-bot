from sqlalchemy import update, select, func, delete
from sqlalchemy.exc import IntegrityError

from utils.db_api.base import async_sessionmaker
from utils.db_api.models.participants import Participants


async def add_participant(telegram_id, username):
    try:
        async with async_sessionmaker() as session:
            await session.merge(Participants(telegram_id=telegram_id, username=username))
            await session.commit()
    except IntegrityError:
        return True

async def get_all_participant():
    async with async_sessionmaker() as session:
        counter = select(func.count('*')).select_from(Participants)
        result = await session.execute(counter)
        for row in result:
            return row[0]

async def get_username_participant():
    array = []
    async with async_sessionmaker() as session:
        counter = select(Participants)
        result = await session.execute(counter)
        for row in result.scalars():
            array.append(row.username)
        return array

async def delete_participants():
    async with async_sessionmaker() as session:
        info = delete(Participants)

        await session.execute(info)
        await session.commit()
