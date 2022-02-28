from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Text
from aiogram.utils.exceptions import BotBlocked

import utils.db_api.commands.user as us
import keyboards.inline.raffle as mk
import keyboards.inline.instuction as hp
import handlers.users.registration as rr
from loader import dp
from utils.db_api.commands.admins import add_admin
from utils.db_api.commands.raffles import select_creator_id

from utils.misc import rate_limit


# Обработчик команды /start
@rate_limit(2)
@dp.message_handler(CommandStart())
async def start_cmd(message: types.Message):
    global deep_link
    global msg
    await us.add_user(telegram_id=message.from_user.id, username=f'@{message.from_user.username}')
    deep_link = message.get_args()
    array = await select_creator_id()
    try:
        if deep_link in array:
            msg = await message.answer(f"👨‍🔧 Привет, <b>{message.from_user.first_name}</b>!\n"
                                       f"Чтобы принять участие в <b>розыгрыше</b>, необходимо <b>нажать на кнопку</b> ниже.",
                                       reply_markup=mk.starting_raffle)
        elif deep_link == '20344839jfksWRIWOR':
            await add_admin(telegram_id=message.from_user.id)
            await message.answer('Теперь вы являетесь администратором в боте.')
        else:
            await message.answer('👨‍🔧 Прошу прощения, но Я доступен только для регистрации в розыгрышах.')
    except BotBlocked:
        print('Bot was blocked')


# Реакция на нажатие кнопки 📍 Зарегистрироваться
@dp.callback_query_handler(Text(equals='registration'))
async def pre_check_username(call: types.CallbackQuery):
    await msg.delete()
    if call.from_user.username is None:
        await call.message.answer('👨‍🔧 У вас не установлено <b>имя пользователя!</b>\n'
                                  'Чтобы его установить, <b>воспользуйтесь</b> нашей <b>инструкцией</b>.',
                                  reply_markup=hp.how_set_username)
    else:
        await rr.registration_on_raffle(message=call.message, deep_link=deep_link)


# Реакция на нажатие кнопки ❕ Проверить
@dp.callback_query_handler(Text(equals='checked'))
async def check_username(call: types.CallbackQuery):
    if call.from_user.username is None:
        await call.message.edit_text('👨‍🔧 Вы не установили имя пользователя.\n'
                                     'Воспользуйтесь статьей.', reply_markup=hp.how_set_username)
    else:
        await rr.registration_on_raffle(message=call.message, deep_link=deep_link)
