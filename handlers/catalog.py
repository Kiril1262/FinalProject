from aiogram import Router, types
from aiomysql import create_pool
from config import config

router = Router()

@router.message(lambda msg: msg.text == "/catalog")
async def show_catalog(message: types.Message):
    async with create_pool(
        host=config.db_config.host,
        port=config.db_config.port,
        user=config.db_config.user,
        password=config.db_config.password,
        db=config.db_config.database
    ) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT id, name FROM categories")
                categories = await cur.fetchall()

                if not categories:
                    return await message.answer("❗ Каталог порожній.")

                for cat_id, cat_name in categories:
                    response = f"<b>📂 {cat_name}</b>\n\n"

                    await cur.execute(
                        "SELECT name, description, price FROM products WHERE category_id = %s",
                        (cat_id,)
                    )
                    products = await cur.fetchall()

                    if products:
                        for name, desc, price in products:
                            desc = desc or "Без опису"
                            price = price or 0.00
                            response += (
                                f"• <b>{name}</b>\n"
                                f"{desc}\n"
                                f"💵 {price} грн\n"
                                f"👉 /order_{name.replace(' ', '_')}\n\n"
                            )
                    else:
                        response += "Наразі немає товарів у цій категорії."

                    await message.answer(response, parse_mode="HTML")

@router.message(lambda m: m.text.startswith("/order_"))
async def handle_order(message: types.Message):
    product_name = message.text.replace("/order_", "").replace("_", " ")
    await message.answer(
        f"📦 Ви обрали товар: <b>{product_name}</b>\n"
        f"Наш менеджер незабаром зв'яжеться з вами!",
        parse_mode="HTML"
    )
