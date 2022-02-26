from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

finish_registration = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text='Завершить регистрацию', callback_data='finish')
    ]
])