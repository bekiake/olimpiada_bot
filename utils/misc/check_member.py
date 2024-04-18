from typing import Union
from aiogram import Bot
from aiogram.types import ChatMember
from aiogram.utils.exceptions import ChatNotFound, BotBlocked, UserDeactivated, TelegramAPIError

async def check(user_id: int, channel: Union[int, str]) -> bool:
    # print({channel})
    bot = Bot.get_current()
    try:
        # Attempt to get the chat member
        member: ChatMember = await bot.get_chat_member(user_id=user_id, chat_id=channel)
        # Check if the user is a member of the chat
        return member.is_chat_member()
    except (ChatNotFound, BotBlocked, UserDeactivated):
        # Handle specific exceptions where the bot can't access the chat or the user
        print(f"Failed to retrieve chat member for channel {channel}: Chat not found or bot blocked/user deactivated.")
        return False
    except TelegramAPIError as e:
        # Handle other Telegram API errors
        print(f"An error occurred with the Telegram API: {e}")
        return False
