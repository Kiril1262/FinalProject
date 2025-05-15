from aiomysql import create_pool
from config import DBConfig, config

async def insert_feedback(user_id: int, feedback_text: str):
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
                    INSERT INTO feedback (user_id, feedback_text)
                    VALUES (%s, %s)
                """, (user_id, feedback_text))
                await conn.commit()
