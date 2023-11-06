import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

import buttons.buttons
import registrations.registration
import user.user_panel
from registrations.registration import *




async def main():
    bot = Bot(token='6946925296:AAHqpeenSDI6WsKFTM9YxzxfCHm_z9idAV4')
    dp = Dispatcher()
    dp.include_routers(registrations.registration.router, user.user_panel.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())