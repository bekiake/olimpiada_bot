from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from states.user_data import UserDataState
from loader import dp,db
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.default import menu

@dp.message_handler(text="Test ishlash")
async def start_test(message:types.Message, state : FSMContext):
    await message.answer("Enter special code:")
    await state.set_state("Code")
@dp.message_handler(state="Code")
async def test_start(message:types.Message, state : FSMContext):
    data = await state.get_data()
    
    try:
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
                if status.get('status'):
                    await message.answer("Javoblaringizni kiritng:")
                    await state.set_state("answer")
                else:
                    await message.answer("Test tugagan yoki endi boshlanadi kanalimizdan xabardor boling!")
                    await state.set_state("Code")
            else:
                await message.answer("Siz bu testni allaqachon ishlagansiz !\nIltimos keyingi testlarni kuting!")
                await state.set_state("Code")
        else:
            await message.answer("Bu raqamli test mavjud emas!")
            await state.set_state("Code")  
        
    except ValueError:
        # If the conversion fails, handle the error gracefully
        await message.answer("Test kodini tekshiring!")
        await state.set_state("Code")
    

        
        
    
    
@dp.message_handler(state='answer')
async def check_test(message:types.Message, state : FSMContext):
    answ = message.text.lower()
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
        for i in range(len(user_answer)):
            if test_answer[i]==user_answer[i]:
                trues += 1
        fish = message.from_user.full_name
        tg_id = str(message.from_user.id)
        answers = trues
        k = int(data.get('code'))
        await db.add_results(fish=fish, telegram_id=tg_id,answers=answers, code=k)
        await message.answer(f"Natijangiz:\nJami savollar:{len(test_answer)}\nTo'g'ri javoblar:{trues} ✅\nNoto'g'ri javoblar:{len(test_answer)-trues}❌")
    else:
        await message.answer("Kiritlgan javoblar soni Savollar sonidan ko'p❗️\nIltimos tekshirib qaytadan yuboring")
        await state.set_state('answer')   
        
    await state.finish()
            
    