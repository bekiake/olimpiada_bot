from aiogram import Dispatcher
from . import is_admin, is_subscriber
from loader import dp
# from .is_admin import AdminFilter


if __name__ == "filters":
    dp.filters_factory.bind(is_admin.AdminFilter)
    dp.filters_factory.bind(is_subscriber.SubscriberFilter)
