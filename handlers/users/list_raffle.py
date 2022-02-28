import aiofiles
from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, bot
from utils.create_txt import insert_txt


@dp.callback_query_handler(Text(equals='list_raffles'))
async def create_list_raffles(call: types.CallbackQuery):
    await insert_txt()
    async with aiofiles.open('розыгрыши.txt', mode='rb') as f:
        await bot.send_document(call.message.chat.id, f,
                                caption='Все активные розыгрыши находятся в данном списке.')
        f.close()