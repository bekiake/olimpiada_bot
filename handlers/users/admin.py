import asyncio
import datetime
import re
from aiogram import types
from aiogram import filters
from aiogram.dispatcher.filters.builtin  import CommandStart
from loader import dp,db
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove
from keyboards.default.menu import admin_btn,start_test
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from loader import bot
from filters import is_admin
from states.olimpics_data import OlimpicsDataState

@dp.message_handler(text="Create Test", user_id = ADMINS)
async def create_olimpics(message:types.Message):
    await message.answer("Enter special code:")
    await OlimpicsDataState.code.set()

@dp.message_handler(state = OlimpicsDataState.code)
async def get_olimpics_code(message: types.Message, state : FSMContext):
    exists_code = await db.check_code(int(message.text))
    if exists_code:
        await message.answer("This code is already used !\nTry another code:")
        await OlimpicsDataState.code.set()
    else:
        code = int(message.text)
    
        await state.update_data(
            {
                'code' : code
            }
        )
        
        await message.answer("Enter File questions:")
        await OlimpicsDataState.photo.set()

@dp.message_handler(state = OlimpicsDataState.photo, content_types=types.ContentType.DOCUMENT)
async def get_photo_olimpcs(message: types.Message, state : FSMContext):
    document = message.document.file_id
    
    await state.update_data(
        {
            'document' : document
        }
    )
    await message.answer("Enter True Answers:")
    await OlimpicsDataState.true_answers.set()

@dp.message_handler(state = OlimpicsDataState.true_answers)
async def get_true_answers(message: types.Message, state : FSMContext):
    answers = []
    answers = message.text.lower().strip().split('\n') 
    true_answers = [re.sub('^\d+\.?', '', item) for item in answers]
    # print(true_answers)
    await state.update_data(
        {
            'true_answers' : true_answers
        }
    )
    await message.answer("Enter Start Time:")
    await OlimpicsDataState.start_time.set()
    

@dp.message_handler(state=OlimpicsDataState.start_time)
async def get_start_time(message: types.Message, state : FSMContext):
    
    #datetime.datetime(2024, 4, 16, 15, 30, 0)
    time = message.date
    yy = int(time.strftime("%Y"))
    mo = int(time.strftime("%m"))
    dd = int(time.strftime("%d"))
    hh = int(message.text.split(":")[0])
    mm = int(message.text.split(":")[1])
    start_time = datetime.datetime(yy,mo,dd,hh,mm,0)
    if start_time<=time:
        await message.answer('Enter correct start time (start time > current time) !')
        await OlimpicsDataState.start_time.set()
    else:
        await state.update_data(
        {
            'start_time' : start_time
        }
        )
        await message.answer("Enter End Time:")
        await OlimpicsDataState.end_time.set()
        
    
    
    
@dp.message_handler(state=OlimpicsDataState.end_time)
async def get_start_time(message: types.Message, state : FSMContext):
    
    #datetime.datetime(2024, 4, 16, 15, 30, 0)
    time = message.date
    yy = int(time.strftime("%Y"))
    mo = int(time.strftime("%m"))
    dd = int(time.strftime("%d"))
    hh = int(message.text.split(":")[0])
    mm = int(message.text.split(":")[1])
    end_time = datetime.datetime(yy,mo,dd,hh,mm,0)
    data = await state.get_data()
    start = data.get('start_time')
    if start>time and end_time>start:
        await state.update_data(
            {
                'end_time' : end_time
            }
        )
        end = data.get('end_time')
        start = data.get('start_time')
        
        data = await state.get_data()
        await db.add_olimpics(data.get('code'), data.get('true_answers'), data.get('start_time'), data.get('end_time'), data.get('document'))
        sand_timer = await message.answer("⏳",reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(0.1)
        await sand_timer.delete()
        btn = InlineKeyboardMarkup(row_width=1)
        btn.insert(InlineKeyboardButton(text=f"Testni yakunlash", callback_data=f"{data.get('code')}"))
        await message.answer(f"<b>code of {data.get('code')} added succesfully !</b>\nTugatish uchun quyidagi tugmani bosing ",parse_mode='HTML', reply_markup=btn)
        await bot.send_message(chat_id=-1001899013345,text=f"🏆<b>Code of {data.get('code')} Olimpic started!</b>\n\n<b>Start time: {data.get('start_time')}</b>\n<b>End time: {data.get('end_time')}</b>\n\n<b>Example for answers:</b>\n<code>a\napple\n2024\netc..</code>", parse_mode='HTML', reply_markup=start_test)
        await state.finish()
    else:
        await message.answer('Enter correct end time:(end time > start time !)')
        await OlimpicsDataState.end_time.set()
    
# @dp.message_handler(text="Last Test Results",state=None ,user_id = ADMINS)
# async def get_last_test_results(message: types.Message, state : FSMContext):
#     await message.answer("code")
#     await state.set_state("Test_kodi")
# @dp.message_handler(state="Test_kodi")
# async def test(message: types.Message, state : FSMContext):
    
    
    
#     try:
#         # Attempt to convert the message text to an integer
#         code = int(message.text)
#         print(code)
#         true_answer = await db.get_true_answers(code)
#         print(true_answer)
#         answer = true_answer.get('true_answers')
#         print(answer)
        
#         # If successful, proceed with the logic for retrieving last test results
#         # Your logic here...
        
#     except ValueError:
#         # If the conversion fails, handle the error gracefully
#         await message.answer("Please provide a valid code as an integer.")
#     # true_answer = await db.get_true_answers(code)
    # print(true_answer)