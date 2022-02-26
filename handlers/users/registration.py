from aiogram import types
from aiogram.dispatcher.filters import Text

from keyboards.inline.check_sub import check, channel
from keyboards.inline.finish import finish_registration
from loader import dp
import utils.check_member as ch


async def registration_on_raffle(message: types.Message):
    await message.answer('👨‍🔧 Для регистрации в розыгрыше, <b>Вам</b> необходимо:\n'
                         '<b><i>- быть подписчиком нашего канала,</i></b>\n'
                         '<b><i>- являться участником нашего чата.</i></b>\n', reply_markup=check)


# Проверяем подписки на чат и канал
@dp.callback_query_handler(Text(startswith='checking_subscribe'))
async def checking_subscribe(call: types.CallbackQuery):
    check_sub = await ch.check_member_channel(user_id=call.from_user.id)
    if check_sub is True:

        await call.answer('Вы успешно подписались на Чат и Канал!', show_alert=True)
        await continue_registration(call=call)
    else:
        await call.answer('Вы не выполнили условие', show_alert=True)


# Функция для продолжения регистрации
async def continue_registration(call: types.CallbackQuery):
    amount = 0
    await call.message.edit_text('👨‍🔧 Если <b>вы</b> стали <b>победителем</b>, '
                                 f'то вам необходимо предоставить чек на сумму {amount} рублей <b>в нашем магазине.</b>',
                                 reply_markup=finish_registration)


# Кнопка для Завершения Регистрации
@dp.callback_query_handler(Text(equals='finish'))
async def finish_reg(call: types.CallbackQuery):
    data = '16/04/2022'
    await call.message.edit_text('👨‍🔧 Вы успешно завершили регистрацию.\n'
                                 f'Ваш ID: {call.from_user.id}\n'
                                 f'Ваш Username: {call.from_user.username}\n\n'
                                 f'Итоги будут известны - {data}\n'
                                 f'Следи за новостями в нашем канале',
                                 reply_markup=channel)
