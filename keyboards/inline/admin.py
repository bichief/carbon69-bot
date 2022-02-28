from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_keyboard = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(text='Розыгрыши', callback_data='raffles_menu')
    ],
    [
        InlineKeyboardButton(text='Рассылка', callback_data='mailing'),
        InlineKeyboardButton(text='Пользователи', callback_data='users')
    ],
    [
        InlineKeyboardButton(text='Очистить список участников', callback_data='delete_participants')
    ]
])

channel_post = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text='Опубликовать', callback_data='channel_post'),
        InlineKeyboardButton(text='Удалить розыгрыш', callback_data='channel_delete')
    ]
])

raffles_menu = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(text='Создать розыгрыш', callback_data='create_raffle'),
    ],
    [
        InlineKeyboardButton(text='Список розыгрышей', callback_data='list_raffles')
    ],
    [
        InlineKeyboardButton(text='Подвести итоги', callback_data='finish_raffle')
    ],

    [
        InlineKeyboardButton(text='Назад', callback_data='go_back')
    ]
])

go_menu = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(text='Назад', callback_data='go_back')
    ]
])


post_users = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text='Да', callback_data='post_yes'),
        InlineKeyboardButton(text='Нет', callback_data='post_no')
    ]
])

users_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text='Добавить админа', switch_inline_query='new_administrator')
    ]
])


delete = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text='Да', callback_data='delete_yes'),
        InlineKeyboardButton(text='Нет', callback_data='delete_no')
    ]
])
