from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from config import config  # config: містить bot_token і db_config
from init_db import init_db

# 📥 Імпортуємо всі обробники
from handlers import (
    start, help, about, contact, catalog,
    admin_add_product, orders, feedback, menu  # Додали menu
)

async def main():
    # 🗃️ Ініціалізація бази даних
    await init_db(config.db_config)

    # 🤖 Ініціалізація бота
    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode="HTML"))

    # 🧠 Ініціалізація сховища FSM
    storage = MemoryStorage()

    # 🎛️ Створення диспетчера з FSM
    dp = Dispatcher(storage=storage)

    # 🔌 Підключення роутерів
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(about.router)
    dp.include_router(contact.router)
    dp.include_router(catalog.router)
    dp.include_router(admin_add_product.router)
    dp.include_router(orders.router)
    dp.include_router(feedback.router)
    dp.include_router(menu.router)  # Підключено menu

    # 🚀 Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())







