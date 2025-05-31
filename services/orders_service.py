from aiomysql import create_pool
from config import config

async def insert_order(data, user_id):
    async with create_pool(
        host=config.db_config.host,
        port=config.db_config.port,
        user=config.db_config.user,
        password=config.db_config.password,
        db=config.db_config.database
    ) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO orders (product_name, quantity, customer_name, phone_number, status, user_id)
                    VALUES (%s, %s, %s, %s, 'pending', %s)
                """, (data["product_name"], data["quantity"], data["customer_name"], data["phone_number"], user_id))
                await conn.commit()
                await cur.execute("SELECT LAST_INSERT_ID()")
                order_id = await cur.fetchone()
    return order_id[0]

async def get_order_status(order_id):
    async with create_pool(
        host=config.db_config.host,
        port=config.db_config.port,
        user=config.db_config.user,
        password=config.db_config.password,
        db=config.db_config.database
    ) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT status FROM orders WHERE order_id = %s", (order_id,))
                result = await cur.fetchone()
    return result[0] if result else None

async def update_order_status(order_id, status):
    async with create_pool(
        host=config.db_config.host,
        port=config.db_config.port,
        user=config.db_config.user,
        password=config.db_config.password,
        db=config.db_config.database
    ) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("UPDATE orders SET status = %s WHERE order_id = %s", (status, order_id))
                await conn.commit()
                await cur.execute("SELECT user_id FROM orders WHERE order_id = %s", (order_id,))
                result = await cur.fetchone()
    return result[0] if result else None

async def get_pending_orders():
    async with create_pool(
        host=config.db_config.host,
        port=config.db_config.port,
        user=config.db_config.user,
        password=config.db_config.password,
        db=config.db_config.database
    ) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT order_id, product_name, status FROM orders WHERE status = 'pending'")
                return await cur.fetchall()

async def get_order_details(order_id):
    async with create_pool(
        host=config.db_config.host,
        port=config.db_config.port,
        user=config.db_config.user,
        password=config.db_config.password,
        db=config.db_config.database
    ) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT product_name, quantity, customer_name, phone_number, status FROM orders WHERE order_id = %s", (order_id,))
                return await cur.fetchone()
