from sqlalchemy import update, select, func
from sqlalchemy.exc import IntegrityError

from utils.db_api.base import async_sessionmaker
from utils.db_api.models.user import User


async def add_user(telegram_id, username):
    try:
        async with async_sessionmaker() as session:
            await session.merge(User(telegram_id=telegram_id, username=username))
            await session.commit()
    except IntegrityError:
        return True


async def get_all_users():
    async with async_sessionmaker() as session:
        counter = select(func.count('*')).select_from(User)
        result = await session.execute(counter)
        for row in result:
            return row[0]


async def get_all_users_for_mailing():
    async with async_sessionmaker() as session:
        array = []
        counter = select(User)
        result = await session.execute(counter)
        for row in result.scalars():
            array.append(row.telegram_id)
        return array



async def get_users_for_txt():
    array = []
    async with async_sessionmaker() as session:
        sql = select(User)
        result = await session.execute(sql)
        for row in result.scalars():
            array.append(f'{row.telegram_id} - {row.username}')
        return array


async def get_all_users_mailing():
    array = []
    async with async_sessionmaker() as session:
        sql = select(User)
        result = await session.execute(sql)
        for row in result.scalars():
            array.append(row.telegram_id)
        return array
