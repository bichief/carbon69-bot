from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text='Канал', url='https://t.me/carbon69channel'),
        InlineKeyboardButton(text='Чат', url='https://t.me/+JXgBLdp-5100ZGUy'),
    ],
    [
        InlineKeyboardButton(text='Проверить', callback_data='checking_subscribe')
    ]
])
channel = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text='Перейти в канал', url='t.me/carbon69channel')
    ]
])