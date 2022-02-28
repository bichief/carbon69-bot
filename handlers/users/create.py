# Обработчик кнопки "Создать розыгрыш"
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from data.config import channel
from keyboards.inline.admin import channel_post
from loader import dp
from states.administator import Admin
import utils.db_api.commands.raffles as db


@dp.callback_query_handler(Text(equals='create_raffle'))
async def create_raffle(call: types.CallbackQuery):
    await call.message.edit_text('Для создания розыгрыша необходимо:\n'
                                 '- дата розыгрыша,\n'
                                 '- сумма чека\n\n'
                                 'Сперва, <b>введите дату</b>\n'
                                 'Пример: 30 ферваля.',
                                 )
    await Admin.get_date.set()


# Получаем дату для БД.
@dp.message_handler(state=Admin.get_date)
async def get_date(message: types.Message, state: FSMContext):
    date = message.text
    check = await db.insert_date(telegram_id=message.from_user.id, date=date)
    if check is True:
        await message.answer('За вами уже закреплен розыгрыш.\n')
        await state.reset_state()
    else:
        await message.answer('Дата успешно введена.\n'
                             'Теперь, введите <b>необходимую сумму чека</b>\n'
                             'Пример: 1000 рублей')
    await Admin.get_amount.set()


@dp.message_handler(state=Admin.get_amount)
async def get_amount(message: types.Message):
    amount = message.text
    await db.insert_amount(telegram_id=message.from_user.id, amount=amount)
    await message.answer('Сумма успешно обновлена.\n'
                         'Теперь необходимо написать текст для поста в канал (можно добавить фото), указав призовые места.\n\n'
                         'Дату и Ссылку Бот впишет самостоятельно!'
                         )
    await Admin.get_text.set()


@dp.message_handler(state=Admin.get_text, content_types=['photo', 'text'])
async def get_text(message: types.Message, state: FSMContext):
    date = await db.select_date(telegram_id=message.from_user.id)
    amount = await db.select_amount(telegram_id=message.from_user.id)

    link = f't.me/Carbon69Bot?start={message.from_user.id}'

    if message.photo:
        text = message.caption
        file_id = message.photo[-1].file_id
        await message.answer('Ваш текст для поста имеет следующий вид:')
        await message.answer_photo(photo=file_id, caption=f'{text}\n\n'
                                                          f'📆 Дата проведения розыгрыша - {date}\n'
                                                          f'📍 Принять участие - {link}', reply_markup=channel_post)
    else:
        text = message.text
        await message.answer('Ваш текст для поста имеет следующий вид:')
        await message.answer(
            f'{text}\n\n'
            f'📆 Дата проведения розыгрыша - {date}\n'
            f'📍 Принять участие - {link}', reply_markup=channel_post)
    await state.reset_state()


@dp.callback_query_handler(Text(startswith='channel_'))
async def public_or_delete(call: types.CallbackQuery):
    data = call.data.split('_')
    if data[1] == 'post':
        target_channel = channel
        message = await call.message.edit_reply_markup()
        await message.send_copy(chat_id=target_channel)
        await call.answer('Пост успешно опубликован!')

    elif data[1] == 'delete':
        await db.delete_raffle(telegram_id=call.from_user.id)
        await call.answer('Розыгрыш успешно удален!')
