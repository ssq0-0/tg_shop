import asyncio
from aiogram import Bot, Dispatcher 
from config.token import token
import registrations.registration
import user.user_panel


async def main():
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_routers(registrations.registration.router, user.user_panel.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
