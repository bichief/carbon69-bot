import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.users.admin import login_cmd
from keyboards.inline.admin import post_users, channel_post
from loader import dp
from states.administator import Admin
from utils.db_api.commands.participants import get_username_participant


@dp.callback_query_handler(Text(equals='finish_raffle'))
async def finish_with_raffle(call: types.CallbackQuery):
    await call.message.edit_text('Отлично!\n'
                                 'Пришло время подвести итоги.\n'
                                 'Отправь мне количество призовых мест!')

    await Admin.get_people.set()


@dp.message_handler(state=Admin.get_people)
async def get_winners(message: types.Message, state: FSMContext):
    global text
    amount = int(message.text)
    array = []
    for i in range(amount):
        users = await get_username_participant()
        winner = random.choice(users)
        array.append(f'{i + 1} место - {winner}')
    text = ''
    for row in array:
        text += f'{row}\n'
    await message.answer(f'{text}\n\n\n'
                         f'Желаете опубликовать итоги в канале?', reply_markup=post_users)
    await state.reset_state()

@dp.callback_query_handler(Text(startswith='post_'))
async def post_winners(call: types.CallbackQuery):
    data = call.data.split('_')
    if data[1] == 'yes':
        await call.message.edit_text('Ваш текст будет выглядеть следующим образом:')
        await call.message.answer('Подведены итоги розыгрыша.\n'
                                  'Победители:\n'
                                  f'{text}\n\n'
                                  f'С вами свяжутся до получения приза.\n'
                                  f'текст если что отредактируем)', reply_markup=channel_post)
    else:
        await call.answer('На нет и суда нет.', show_alert=True)
        await login_cmd(message=call.message)
