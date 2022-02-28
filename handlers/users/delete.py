import aiofiles
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp, bot
from states.administator import Admin
from utils.create_txt import insert_txt
from utils.db_api.commands.raffles import delete_raffle_by_id


@dp.callback_query_handler(Text(equals='delete_raffle'))
async def delete_raf(call: types.CallbackQuery):
    await insert_txt()
    async with aiofiles.open('розыгрыши.txt', mode='rb') as f:
        await bot.send_document(call.message.chat.id, f,
                                caption='Введите ID розыгрыша, необходимого для удаления.')
        f.close()
        await Admin.get_id.set()

@dp.message_handler(state=Admin.get_id)
async def get_id(message: types.Message, state: FSMContext):
    text = message.text
    await delete_raffle_by_id(text)
    await state.reset_state()
    await message.answer('Розыгрыш успешно удален!')