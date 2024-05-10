import asyncio
import logging
import sys
from config import dp,bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from throttling import ThrottlingMiddleware
from check_user import User_checkMiddleware

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text="TEST", callback_data="check")
    await message.answer(f"HELLO", reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data == 'check')
async def callback_query_handler(call: CallbackQuery) -> None:
    await call.message.answer("TEST")

@dp.message()
async def command_start_handler(message: Message) -> None:
    await message.answer(message.text)

async def main():
    dp.message.middleware.register(ThrottlingMiddleware())
    dp.update.middleware.register(User_checkMiddleware())
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())