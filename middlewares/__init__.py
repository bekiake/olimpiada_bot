from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .subscription_channel import CheckMemberMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CheckMemberMiddleware())
    
