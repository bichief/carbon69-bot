import asyncio
import re
import datetime

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest

from filters.admin import AdminFilter
from filters.group import IsGroup
from filters.russian_filter import check_message
from loader import dp, bot

restriction_time_regex = re.compile(r'(\b[1-9][0-9]*)([mhds]\b)')


def get_restriction_period(text: str) -> int:
    if match := re.search(restriction_time_regex, text):
        time, modifier = match.groups()
        multipliers = {"m": 60, "h": 3600, "d": 86400, "s": 1}
        return int(time) * multipliers[modifier]
    return 0


@dp.message_handler(IsGroup(), AdminFilter(), regexp=r"(!ro|/ro) ?(\b[1-9][0-9]\w)? ?([\w+\D]+)?")
async def read_only(message: types.Message):
    global information
    (
        admin_username,
        admin_mentioned,
        chat_id,
        member_id,
        member_username,
        member_mentioned,
    ) = get_members_info(message)

    command_parse = re.compile(r"(!ro|/ro) ?(\b[1-9][0-9]\w)? ?([\w+\D]+)?")
    parsed = command_parse.match(message.text)
    reason = parsed.group(3).split(' ')
    really_reason = reason[1]

    really_reason = "без указания причины" if not really_reason else f"по причине: {really_reason}"

    ro_period = get_restriction_period(message.text)
    ro_end_date = message.date + datetime.timedelta(seconds=ro_period)

    ReadOnlyPerm = types.ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_other_messages=False,
        can_send_polls=False,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False
    )

    try:
        # Пытаемся забрать права у пользователя
        await message.chat.restrict(
            user_id=member_id,
            permissions=ReadOnlyPerm,
            until_date=ro_end_date,
        )

        # Отправляем сообщение
        information = await message.answer(
            f"Пользователю {member_mentioned} "
            f"было запрещено писать до {ro_end_date.strftime('%d.%m.%Y %H:%M')}\n "
            f"администратором {admin_mentioned}\n"
            f"{really_reason} "
        )


    except BadRequest:
        await message.answer(
            f"Пользователь {member_mentioned} "
            "является администратором чата, я не могу выдать ему RO"
        )

    service_message = await message.reply(
        'Сообщение самоуничтожится через 5 секунд.'
    )

    await asyncio.sleep(5)
    # после прошедших 5 секунд, бот удаляет сообщение от администратора и от самого бота
    await message.delete()
    await service_message.delete()
    await message.reply_to_message.delete()


@dp.message_handler(
    IsGroup(),
    Command(commands=["unro"], prefixes="!/"), AdminFilter()
)
async def undo_read_only_mode(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !unro ИЛИ /unro"""
    (
        admin_username,
        admin_mentioned,
        chat_id,
        member_id,
        member_username,
        member_mentioned,
    ) = get_members_info(message)

    perm = types.ChatPermissions(can_send_messages=True,
                                 can_send_media_messages=True,
                                 can_send_polls=False,
                                 can_send_other_messages=True,
                                 can_add_web_page_previews=True,
                                 can_invite_users=False,
                                 can_change_info=False,
                                 can_pin_messages=False)

    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=member_id,
        permissions=perm,
    )

    # Информируем об этом
    information = await message.answer(
        f"Пользователь {member_mentioned} был размучен администратором {admin_mentioned}"
    )
    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")

    # Пауза 5 сек
    await asyncio.sleep(5)

    # Удаляем сообщения от бота и администратора
    await information.delete()
    await message.delete()
    await service_message.delete()


@dp.message_handler(
    IsGroup(),
    Command(commands=["ban"], prefixes="!/")
)
async def ban_user(message: types.Message):
    admin_mentioned = message.from_user.get_mention(as_html=True)
    member_id = message.reply_to_message.from_user.id
    member_mentioned = message.reply_to_message.from_user.get_mention(as_html=True)
    try:
        # Пытаемся удалить пользователя из чата
        await message.chat.kick(user_id=member_id)
        # Информируем об этом
        await message.answer(
            f"Пользователь {member_mentioned} был успешно забанен администратором {admin_mentioned}"
        )

    except BadRequest:
        # Отправляем сообщение
        await message.answer(
            f"Пользователь {member_mentioned} "
            "является администратором чата, я не могу выдать ему RO"
        )

    service_message = await message.answer("Сообщение самоуничтожится через 5 секунд.")

    # После чего засыпаем на 5 секунд
    await asyncio.sleep(5)
    # Не забываем удалить сообщение, на которое ссылался администратор
    await message.reply_to_message.delete()
    await message.delete()
    await service_message.delete()

@dp.message_handler(
    IsGroup(),
    Command(commands=["unban"], prefixes="!/"),

)
async def unban_user(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !unban ИЛИ /unban"""

    # Создаем переменные для удобства
    admin_mentioned = message.from_user.get_mention(as_html=True)
    member_id = message.reply_to_message.from_user.id
    member_mentioned = message.reply_to_message.from_user.get_mention(as_html=True)

    # И разбаниваем
    await message.chat.unban(user_id=member_id)

    # Пишем в чат
    await message.answer(
        f"Пользователь {member_mentioned} был разбанен администратором {admin_mentioned}"
    )
    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")

    # Пауза 5 сек
    await asyncio.sleep(5)



    # Удаляем сообщения
    await message.delete()
    await service_message.delete()


@dp.message_handler(content_types=['text'])
async def checking_text_russian(message: types.Message):
    author = message.from_user.get_mention(as_html=True)
    state = check_message(text=message.text)
    if state is True:
        await message.reply(f'{author}, не матерись!')
    else:
        pass


def get_members_info(message: types.Message):
    # Создаем переменные для удобства
    return [
        message.from_user.username,
        message.from_user.get_mention(as_html=True),
        message.chat.id,
        message.reply_to_message.from_user.id,
        message.reply_to_message.from_user.username,
        message.reply_to_message.from_user.get_mention(as_html=True),
    ]
