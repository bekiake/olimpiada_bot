from typing import Union
from aiogram import Bot
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import ChatMember
from aiogram.utils.exceptions import ChatNotFound, BotBlocked, UserDeactivated, TelegramAPIError

class SubscriberFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        chanel = "-1001899013345"
        bot = Bot.get_current()
        try:
            member = await bot.get_chat_member(user_id=message.from_user.id, chat_id=chanel)
            return member.is_chat_member()
        except (ChatNotFound, BotBlocked, UserDeactivated):
            print(f"Failed to retrieve chat member for channel {chanel}: Chat not found or bot blocked/user deactivated.")
            return False
        except TelegramAPIError as e:
            print(f"An error occurred with the Telegram API: {e}")
            return False  
