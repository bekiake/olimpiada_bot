import re
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from states.user_data import UserDataState
from loader import dp,db
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.default import menu
import datetime
from loader import bot

@dp.message_handler(text="Test ishlash")
async def start_test(message:types.Message, state : FSMContext):
    count_ref = await db.count_ref(user_id=str(message.from_user.id))
    if count_ref.get('count')>=3:
        await message.answer("<b>Maxsus kodni kiriting(Special code):</b>", parse_mode='HTML')
        await state.set_state("Code")
    else:
        await message.answer(f"Siz hali 3ta do'stingizni chaqirmadingiz!\nSizning referallaringiz soni {count_ref.get('count')}\n\n Do'stlarga ulashish uchun:\n<code>https://t.me/karimovs_olimpic_bot?start={message.from_user.id}</code>", reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("Ulashish ♻️", url=f"https://t.me/share/url?url=https://t.me/karimovs_olimpic_bot?start={message.from_user.id}")))
@dp.message_handler(state="Code")
async def test_start(message:types.Message, state : FSMContext):
    data = await state.get_data()
    
    if message.text.isdigit():
        code = int(message.text)
    
        check_code = await db.check_code(code=code)
        if check_code is not None:
            user = str(message.from_user.id)
            check_user = await db.check_result_user(telegram_id=user,code=code)
            if check_user is None:
                await state.update_data(
                    {'code':message.text}
                    )
                status = await db.check_status(code)
                start = status.get('time_start')
                end = status.get('time_end')
                time = message.date
                # print(status.get('status'))
                p = await db.get_olimpic_photo(code=code)
                photo = p.get('photo')
                # print(photo)
                if start<=time<=end and status.get('status'):
                    await bot.send_document(chat_id=message.from_user.id, document=photo, caption='<b>Javoblaringizni kiritng:</b>', parse_mode='HTML')
                    await state.set_state("answer")
                elif time<=start:
                    await message.answer("Test endi boshlanadi kanalimizdan xabardor boling!")
                    await state.finish()
                elif time>end or (not status.get('status')):
                    await message.answer("Test tugab bo'lgan!\nKeyingi testlarimizda chaqqonroq bo'ling va kanalimizdan xabardor bo'ling")
                    await state.finish()
            else:
                await message.answer("Siz bu testni allaqachon ishlagansiz !\nIltimos keyingi testlarni kuting!")
                await state.finish()
        else:
            await message.answer("Bu raqamli test mavjud emas!")
            await state.finish()
            
        
    else:
            await message.answer("Test kodini tekshiring va qaytadan 'Test ishlash' tugmasini bosing")
            await state.finish()

        
        
    
    
@dp.message_handler(state='answer')
async def check_test(message:types.Message, state : FSMContext):
    correct = message.text.lower().strip().split('\n')
    answ = [re.sub('^\d+\.?', '', item) for item in correct]
    # print(answ)
    await state.update_data(
            {
                'user_answer' : answ
            }
            )
    data = await state.get_data()
    t_answers = await db.get_true_answers(int(data.get('code')))
    test_answer = t_answers.get('true_answers')
    user_answer = data.get('user_answer')
    
    if len(test_answer) >= len(user_answer):
        trues=0
        result = ""
        for i in range(len(user_answer)):
            if test_answer[i]==user_answer[i]:
                trues += 1
                result += f"{i+1}. {user_answer[i]} ✅\n"
            else:
                result += f"{i+1}. {user_answer[i]} ❌\n"
        fish = message.from_user.full_name
        tg_id = str(message.from_user.id)
        answers = trues
        k = int(data.get('code'))
        await db.add_results(fish=fish, telegram_id=tg_id,answers=answers, code=k)
        await message.answer(f"Natijangiz:\n{result}\nJami savollar:{len(test_answer)}\nTo'g'ri javoblar:{trues} ✅\nNoto'g'ri javoblar:{len(test_answer)-trues}❌")
    else:
        await message.answer("Kiritlgan javoblar soni Savollar sonidan ko'p❗️\nIltimos tekshirib qaytadan yuboring")
        await state.set_state('answer')   
        
    await state.finish()
            

@dp.message_handler(text="Mening Referallarim")
async def get_user_referals(message:types.Message):
    count_ref = await db.count_ref(user_id=str(message.from_user.id))
    await message.answer(f"Sizning referallaringiz soni: <b>{count_ref.get('count')}</b>\nDo'stlarga ulashish uchun:\n\n<code>https://t.me/karimovs_olimpic_bot?start={message.from_user.id}</code>",parse_mode='HTML' ,reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("Ulashish ♻️", url=f"https://t.me/share/url?url=https://t.me/karimovs_olimpic_bot?start={message.from_user.id}")))
    