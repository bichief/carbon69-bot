from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

how_set_username = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text='❕ Ознакомиться', url='https://telegra.ph/Kak-ustanovit-imya-polzovatelya-username-02-26')
    ],
    [
        InlineKeyboardButton(text='❕ Проверить', callback_data='checked')
    ]
])