from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from states.user_data import UserDataState
from loader import dp,db
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.default.menu import kb,phone,admin_btn
from data.config import ADMINS,CHANNEL
from utils.misc.check_member import check



@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await db.cheak_user(str(message.from_user.id))
    ref_count = await db.count_ref(str(message.from_user.id))
    print(ref_count)
    if str(message.from_user.id) in ADMINS:
        await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=admin_btn)
    else:
        if user:
            await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=kb)
        else:
            await message.answer(f"Salom, {message.from_user.full_name}!\nTo'liq ism familiyangizni kiriting! ")
            await UserDataState.fish.set()

@dp.message_handler(state = UserDataState.fish)
async def get_fish(message: types.Message, state : FSMContext):
    fish = message.text
    
    await state.update_data(
        {
            'fish' : fish
        }
    )
    await message.answer(f"Telefon raqamingizni kiriting:", reply_markup=phone)
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
    await db.add_user(data.get('fish'),data.get('tel'), str(message.from_user.id))
    await message.answer("Ro'yxatdan o'tish tugadi!\n Botimizga Xush kelibsiz!",reply_markup=kb)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'check_subs')
async def check_subs(query: types.CallbackQuery):
    user_id = query.from_user.id
    chanel_id = CHANNEL[0]
    
    is_member = await check(user_id=user_id,channel=chanel_id)
    
    
    if is_member:
        await query.message.edit_text('Thank you for subscribing to all required channels.')
        a = await query.message.answer(f"Botimizga xush kelibsiz! Test ishlash uchun 3ta do'stingizni chaqiring\nSizning referalingiz:\nhttps://t.me/karimovs_olimpic_bot?start={user_id}",reply_markup=kb)

