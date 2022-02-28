from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from utils.db_api.base import async_sessionmaker
from utils.db_api.models.raffles import Raffles


async def insert_date(telegram_id, date):
    try:
        async with async_sessionmaker() as session:
            await session.merge(Raffles(creator_id=int(telegram_id), date=date))
            await session.commit()
    except IntegrityError:
        return True


async def insert_amount(telegram_id, amount):
    async with async_sessionmaker() as session:
        info = (
            update(Raffles).where(Raffles.creator_id == int(telegram_id)).values(amount=amount)
        )
        await session.execute(info)
        await session.commit()


async def select_date(telegram_id):
    try:
        async with async_sessionmaker() as session:
            info = select(Raffles).where(Raffles.creator_id == int(telegram_id))

            result = await session.execute(info)

            for row in result.scalars():
                return row.date
    except:
        pass


async def select_creator_id():
    try:
        async with async_sessionmaker() as session:
            info = select(Raffles)
            array = []
            result = await session.execute(info)

            for row in result.scalars():
                array.append(f'{row.creator_id}')
            return array
    except:
        pass


async def select_amount(telegram_id):
    try:
        async with async_sessionmaker() as session:
            info = select(Raffles).where(Raffles.creator_id == int(telegram_id))

            result = await session.execute(info)

            for row in result.scalars():
                return row.amount
    except:
        pass


async def delete_raffle(telegram_id):
    async with async_sessionmaker() as session:
        info = delete(Raffles).where(Raffles.creator_id == int(telegram_id))

        await session.execute(info)
        await session.commit()

async def delete_raffle_by_id(id):
    async with async_sessionmaker() as session:
        info = delete(Raffles).where(Raffles.id == int(id))

        await session.execute(info)
        await session.commit()


async def select_all_raffles():
    async with async_sessionmaker() as session:
        array = []
        info = select(Raffles)

        result = await session.execute(info)

        for row in result.scalars():
            array.append(f'{row.id} | {row.creator_id} | {row.date} | {row.amount}')
        return array

