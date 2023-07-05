import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from handlers import start, profile, announcement_detail, register, create_announcement, language, list_announcement
from config.config_reader import config
from aiogram.fsm.storage.redis import RedisStorage
from aioredis import Redis
from middleware.locale import Localization

redis = Redis()
i18n = I18n(path='locales', default_locale='ua', domain='ApiSwipeBot')



async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.message.outer_middleware(Localization(i18n))
    dp.callback_query.outer_middleware(Localization(i18n))

    dp.include_routers(start.router, profile.router, announcement_detail.router, register.router, create_announcement.router, language.router, list_announcement.router)


    print("BOT WORKING")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

