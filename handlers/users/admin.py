
from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import Command, Text
from aiogram.utils.exceptions import BotBlocked

from keyboards.inline.admin import admin_keyboard, raffles_menu, users_keyboard, delete
from loader import dp, bot

from states.administator import Admin
from utils.db_api.commands.admins import get_all_admins, get_admins
from utils.db_api.commands.participants import get_all_participant, delete_participants
from utils.db_api.commands.user import get_all_users_for_mailing, get_all_users


# Обработчик команды /login
@dp.message_handler(Command('login'))
async def login_cmd(message: types.Message):
    admins = await get_admins()
    if message.from_user.id not in admins:
        await message.answer('Вы не являетесь администратором.')
    else:
        global msg
        msg = await message.answer('Добро пожаловать в админ-меню.\n'
                                   'Воспользуйтесь кнопками для навигации.', reply_markup=admin_keyboard)


# Обработчик меню Розыгрышей
@dp.callback_query_handler(Text(equals='raffles_menu'))
async def menu(call: types.CallbackQuery):
    global mess
    await msg.delete()
    mess = await call.message.answer('Выбери необходимое действие с розыгрышами.', reply_markup=raffles_menu)


# Вернуться в админ-меню
@dp.callback_query_handler(Text(equals='go_back'))
async def goto_login(call: types.CallbackQuery):
    await mess.delete()
    await login_cmd(message=call.message)


# Рассылка пользователям
@dp.callback_query_handler(Text(equals='mailing'))
async def start_mailing(call: types.CallbackQuery):
    await call.message.edit_text('Введите текст для рассылки\n'
                                 '(можно вместе с фото)')
    await Admin.get_mailing.set()


@dp.message_handler(state=Admin.get_mailing, content_types=['photo', 'text'])
async def mailing(message: types.Message, state: FSMContext):
    rows = await get_all_users_for_mailing()
    allowed = 0
    blocked = 0
    if message.photo:
        file_id = message.photo[-1].file_id
        text = message.caption
        try:
            for row in rows:
                await bot.send_photo(
                    chat_id=row,
                    caption=text,
                    photo=file_id
                )
                allowed += 1
        except BotBlocked:
            blocked += 1
    else:
        text = message.text
        try:
            for row in rows:
                await bot.send_message(
                    chat_id=row,
                    text=text
                )
                allowed += 1
        except BotBlocked:
            blocked += 1
    await state.reset_state()
    await message.answer(f'Сообщение доставлено {allowed} пользователям.\n'
                         f'Не получили - {blocked} человек.')


@dp.callback_query_handler(Text(equals='users'))
async def get_users(call: types.CallbackQuery):
    amount_users = await get_all_users()
    amount_participants = await get_all_participant()
    amount_admins = await get_all_admins()
    await call.message.edit_text('<b>INFO</b>\n'
                                 f'Пользователи, авторизовавшиеся в боте - {amount_users}\n'
                                 f'Участники в розыгрыше - {amount_participants}\n'
                                 f'Администраторы - {amount_admins}', reply_markup=users_keyboard)


@dp.callback_query_handler(Text(equals='delete_participants'))
async def delete_part(call: types.CallbackQuery):
    await call.message.edit_text('Вы уверены, что хотите очистить список участников?', reply_markup=delete)

@dp.callback_query_handler(Text(startswith='delete_'))
async def delete_part_two(call: types.CallbackQuery):
    data = call.data.split('_')
    if data[1] == 'yes':
        await delete_participants()
        await call.message.edit_text('Участники были успешно очищены!')
    elif data[1] == 'no':
        await call.answer('На нет и суда нет!', show_alert=True)
    else:
        pass

