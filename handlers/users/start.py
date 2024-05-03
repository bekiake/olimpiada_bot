from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from states.user_data import UserDataState
from loader import dp,db,bot
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.default.menu import kb,phone,admin_btn
from data.config import ADMINS,CHANNEL
from utils.misc.check_member import check


channel = int(CHANNEL[0])
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    user = await db.cheak_user(str(message.from_user.id))    
    ref_id = str(message.text[7:])
    # print(ref_id, "################")
    if len(ref_id) != 0:
        if user:
            await message.answer("Siz oldinroq ro'yxatdan o'tgansiz!", reply_markup=kb)
        else:
            await db.add_ref_user(user_id=ref_id,referal_user_id=str(message.from_user.id))
            
            if await check(user_id=str(message.from_user.id),channel=channel):
                
                await db.update_ref_status(str(message.from_user.id))
            await message.answer(f"Salom {message.from_user.full_name}\n Ism familiyangizni kiriting:")
            # await state.set_state("fish")
            await UserDataState.fish.set()
    
    if user and (user[0]['telegram_id'] in ADMINS):
        await message.answer(f"Salom {message.from_user.full_name}", reply_markup=admin_btn)
    elif user:
        await message.answer(f"salom", reply_markup=kb)
    else:
        await message.answer(f"Salom {message.from_user.full_name}\n Ism familiyangizni kiriting:")
        # await state.set_state("fish")
        await UserDataState.fish.set()
        
       
            
    
        

           






##registration form
@dp.message_handler(state = UserDataState.fish)
async def get_fish(message: types.Message, state : FSMContext):
    fish = message.text
    await state.update_data(
        {
            'fish' : fish
        }
    )
    await message.answer(f"Telefon raqamingizni kiriting:", reply_markup=phone)
    # await state.set_state("tel")
    await UserDataState.tel.set()

@dp.message_handler(state=UserDataState.tel, content_types=types.ContentType.CONTACT)
async def get_tel(message: types.Message, state: FSMContext):
    tel = message.contact.phone_number
    
    await state.update_data(
        {
            'tel' : tel
        }
    )
    data = await state.get_data()
    try:
        await db.add_user(data.get('fish'), data.get('tel'), str(message.from_user.id))
        await message.answer("Ro'yxatdan o'tish tugadi!\n Botimizga Xush kelibsiz!", reply_markup=kb)
        await state.finish()
    except Exception as e:
        await message.answer("Kechirasiz, xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.")
        print(f"Database error: {e}")
#-----------------registration----end


@dp.callback_query_handler(lambda c: c.data == 'check_subs')
async def check_subs(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    chanel_id = CHANNEL[0]
    
    is_member = await check(user_id=user_id,channel=chanel_id)
    
    
    if is_member:
        await db.update_ref_status(str(query.from_user.id))
        await query.message.edit_text('Thank you for subscribing to all required channels.')
        if await db.cheak_user(str(query.from_user.id)):
            a = await query.message.answer(f"Botimizga xush kelibsiz! Test ishlash uchun 3ta do'stingizni chaqiring\nSizning referalingiz:\nhttps://t.me/karimovs_olimpic_bot?start={user_id}",reply_markup=kb)
        else:
            await query.message.answer(f"Salom {query.from_user.full_name}\n Ism familiyangizni kiriting:")
            await UserDataState.fish.set()
