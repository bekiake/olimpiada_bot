from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = KeyboardButton('Test ishlash ')
kb = ReplyKeyboardMarkup(resize_keyboard=True).add(menu)

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
        KeyboardButton(text='Last Test Results')
        ],
    ],resize_keyboard=True
)