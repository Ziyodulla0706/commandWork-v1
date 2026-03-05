from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher
import asyncio
from handlers.mentor import router as mentor_router
from database.db_mentor import init_db
from aiogram.types import BotCommand

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🚀 Запустить бота"),
        BotCommand(command="help", description="❓ Помощь"),
    ]
    await bot.set_my_commands(commands)



load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    print("Bot is running...")
    init_db()
    await set_commands(bot)
    dp.include_router(mentor_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
