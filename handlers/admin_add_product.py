from aiogram import Router, types
from aiomysql import create_pool
from config import config

router = Router()

# 👉 Впиши сюди свій Telegram ID
ADMIN_IDS = [1038982882]  # Замініть на свій ID

@router.message(lambda msg: msg.text.startswith("/add_product "))
async def add_product(message: types.Message):
    # 🔐 Перевірка прав доступу
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("⛔ Ви не маєте прав доступу.")

    try:
        parts = message.text.replace("/add_product ", "").split("|")
        if len(parts) != 4:
            raise ValueError("Неправильний формат.")

        name = parts[0].strip()
        description = parts[1].strip()
        price = float(parts[2].strip())
        category_name = parts[3].strip()

        async with create_pool(
            host=config.db_config.host,
            port=config.db_config.port,
            user=config.db_config.user,
            password=config.db_config.password,
            db=config.db_config.database
        ) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    # 🔍 Пошук категорії
                    await cur.execute("SELECT id FROM categories WHERE name = %s", (category_name,))
                    category = await cur.fetchone()

                    if not category:
                        return await message.answer(
                            f"❗ Категорію <b>{category_name}</b> не знайдено.",
                            parse_mode="HTML"
                        )

                    category_id = category[0]

                    # 💾 Додавання товару
                    await cur.execute(
                        "INSERT INTO products (name, description, price, category_id) VALUES (%s, %s, %s, %s)",
                        (name, description, price, category_id)
                    )
                    await conn.commit()

                    await message.answer(
                        f"✅ Товар <b>{name}</b> додано до категорії <b>{category_name}</b>!",
                        parse_mode="HTML"
                    )

    except Exception:
        await message.answer(
            "⚠️ Помилка під час додавання товару.\n"
            "Формат: /add_product Назва | Опис | Ціна | Категорія"
        )

