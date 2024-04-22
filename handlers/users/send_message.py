import asyncio
import datetime
from aiogram import types
from loader import dp,db,bot



@dp.callback_query_handler()
async def send_message(query: types.CallbackQuery):
    code = int(query.data)
    await db.update_olimpic_status(code=code)
    await query.message.edit_text(f"{code} - raqamli Test muvaffaqiyatli yakunlandi")
    result = await db.get_users_result(code=code)
    text = f"🏆 <b>Test ({code}) yakuniga yetdi!</b>\n\nNatijalar bilan tanishishingiz mumkin:\n\n"
    for i in range(len(result)):
        if i==0:
            text+=f"🥇 - <a href='tg://user?id={result[i][2]}'>{result[i][1]}</a> <b>({result[i][3]}b)</b>\n"
        elif i==1:
            text+=f"🥈 - <a href='tg://user?id={result[i][2]}'>{result[i][1]}</a> <b>({result[i][3]}b)</b>\n"
        elif i==2:
            text+=f"🥉 - <a href='tg://user?id={result[i][2]}'>{result[i][1]}</a> <b>({result[i][3]}b)</b>\n"
        else:
            text+=f"{i+1} - <a href='tg://user?id={result[i][2]}'>{result[i][1]}</a> <b>({result[i][3]}b)</b>\n"
            
            
        
    await bot.send_message(chat_id=1210278389,text=text, parse_mode='HTML')
    await bot.send_message(chat_id=-1001899013345,text=text, parse_mode='HTML')
    
    
    
    
    