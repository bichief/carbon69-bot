from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

starting_raffle = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text='📍 Зарегистрироваться', callback_data='registration')
    ]
])