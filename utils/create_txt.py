import os

import aiofiles

from utils.db_api.commands.raffles import select_all_raffles


async def insert_txt():
    rows = await select_all_raffles()

    if os.path.exists('розыгрыши.txt'):
        os.remove('розыгрыши.txt')

    async with aiofiles.open('розыгрыши.txt', mode='a', encoding='utf-8') as f:
        await f.write('ID | ID создателя | Дата | Сумма чека')
        await f.write('\n')
        for row in rows:
            await f.write(row)
            await f.write('\n')
        f.close()