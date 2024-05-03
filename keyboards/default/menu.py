from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton


kb = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="Test ishlash"),
        KeyboardButton(text="Mening Referallarim")
        ],
    ], resize_keyboard=True
)

phone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📱 Telefon raqamni kiriting', request_contact=True)
        ],
        
    ],resize_keyboard=True
)

admin_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text='Create Test'),
        ],
    ],resize_keyboard=True
)

start_test = InlineKeyboardMarkup(row_width=1)
start_test.insert(InlineKeyboardButton(text="🏆Start Test", url=f"https://t.me/karimovs_olimpic_bot?start"))
