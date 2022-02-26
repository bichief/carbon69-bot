from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Text

import keyboards.inline.raffle as mk
import keyboards.inline.instuction as hp
import handlers.users.registration as rr
from loader import dp


# Обработчик команды /start
@dp.message_handler(CommandStart())
async def start_cmd(message: types.Message):
    global msg
    deep_link = message.get_args()
    if deep_link == '316403137':
        msg = await message.answer(f"👨‍🔧 Привет, <b>{message.from_user.first_name}</b>!\n"
                                   f"Чтобы принять участие в <b>розыгрыше</b>, необходимо <b>нажать на кнопку</b> ниже.",
                                   reply_markup=mk.starting_raffle)
    else:
        await message.answer('👨‍🔧 Прошу прощения, но Я доступен только для регистрации в розыгрышах.')

# Реакция на нажатие кнопки 📍 Зарегистрироваться
@dp.callback_query_handler(Text(equals='registration'))
async def pre_check_username(call: types.CallbackQuery):
    await msg.delete()
    if call.from_user.username is None:
        await call.message.answer('👨‍🔧 У вас не установлено <b>имя пользователя!</b>\n'
                                  'Чтобы его установить, <b>воспользуйтесь</b> нашей <b>инструкцией</b>.',
                                  reply_markup=hp.how_set_username)
    else:
        await rr.registration_on_raffle(message=call.message)


# Реакция на нажатие кнопки ❕ Проверить
@dp.callback_query_handler(Text(equals='checked'))
async def check_username(call: types.CallbackQuery):
    if call.from_user.username is None:
        await call.message.edit_text('👨‍🔧 Вы не установили имя пользователя.\n'
                                     'Воспользуйтесь статьей.', reply_markup=hp.how_set_username)
    else:
        await rr.registration_on_raffle(message=call.message)
