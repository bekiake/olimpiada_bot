import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from data.config import CHANNEL
from utils.misc.check_member import check
from loader import bot,db


class CheckMemberMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data:dict):
        try:
            ref_id = str(update.message.text)[7:]
            client_id = str(update.message.from_user.id)
            user_status = await db.cheak_user(ref_id)
            ch = CHANNEL[0]
            if not user_status:
                await db.add_ref_user(user_id=ref_id,referal_user_id=client_id)
                client_stats = await check(user_id=client_id,channel=ch)
                if client_stats:
                    await db.check_ref_stats(True)
                else:
                    await bot.send_message(chat_id=client_id,text="Siz allaqachon ro'yxatdan o'tgansiz")
        except Exception as e:
            print(e)
        if update.message:
            user = update.message.from_user.id
            # if update.message.text in ['/start','/help']:
            #     return
        elif update.callback_query:
            user = update.callback_query.from_user.id
        else:
            return
        
        logging.info(user)

        result = "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n"
        buttons = InlineKeyboardMarkup(row_width=1)
        final_status = True
        for channel in CHANNEL:
            status = await check(user_id=user,channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)

            if not status:
                buttons.insert(InlineKeyboardButton(text=f"✅ {channel.title}", url=f"{await channel.export_invite_link()}"))

        if not final_status:
            buttons.insert(InlineKeyboardButton(text=f"Tekshirish", callback_data='check_subs'))
            await bot.send_message(chat_id=user,text=result,disable_web_page_preview=True,
                                    reply_markup=buttons)
            raise CancelHandler()
