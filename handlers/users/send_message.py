import asyncio
import datetime
from aiogram import types
from loader import dp,db
from aiogram import Bot


@dp.callback_query_handler()
async def send_message(query: types.CallbackQuery):
    code = int(query.data)
    await db.update_olimpic_status(code=code)
    await query.message.edit_text(f"{code} - raqamli Test muvaffaqiyatli yakunlandi")
    print('aaaaaaa')
    result = await db.get_users_result(code=code)
    print(result)
    
    