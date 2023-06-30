import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import check, profile, announcement_detail

from config.config_reader import config


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(check.router, profile.router, announcement_detail.router)

    print("BOT WORKING")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

