from aiogram import Router, types, F
from aiomysql import create_pool
from config import config

router = Router()


async def fetch_categories(cur):
    await cur.execute("SELECT id, name FROM categories")
    return await cur.fetchall()


async def fetch_products_by_category(cur, cat_id):
    await cur.execute(
        "SELECT name, description, price FROM products WHERE category_id = %s",
        (cat_id,)
    )
    return await cur.fetchall()


def format_product(name, desc, price):
    desc = desc or "Без опису"
    price = price or 0.00
    return (
        f"• <b>{name}</b>\n"
        f"{desc}\n"
        f"💵 {price:.2f} грн\n"
        f"👉 /order_{name.replace(' ', '_')}\n\n"
    )


def format_category_block(cat_name, products):
    response = f"<b>📂 {cat_name}</b>\n\n"
    if products:
        for name, desc, price in products:
            response += format_product(name, desc, price)
    else:
        response += "Наразі немає товарів у цій категорії."
    return response


@router.message(F.text == "/catalog")
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
                categories = await fetch_categories(cur)

                if not categories:
                    return await message.answer("❗ Каталог порожній.")

                for cat_id, cat_name in categories:
                    products = await fetch_products_by_category(cur, cat_id)
                    response = format_category_block(cat_name, products)
                    await message.answer(response, parse_mode="HTML")


@router.message(F.text.startswith("/order_"))
async def handle_order(message: types.Message):
    product_name = message.text.removeprefix("/order_").replace("_", " ")
    await message.answer(
        f"📦 Ви обрали товар: <b>{product_name}</b>\n"
        f"Наш менеджер незабаром зв'яжеться з вами!",
        parse_mode="HTML"
    )
