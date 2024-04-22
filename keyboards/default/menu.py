from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="Test ishlash"),
        KeyboardButton(text="My Referals")
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