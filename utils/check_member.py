from data import config
from loader import bot


async def check_member_channel(user_id):
    user_channel_status = await bot.get_chat_member(chat_id=config.channel, user_id=user_id)
    user_chat_status = await bot.get_chat_member(chat_id=config.chat_id, user_id=user_id)
    if user_channel_status["status"] != 'left' and user_chat_status["status"] != 'left':
        return True
    else:
        return False


