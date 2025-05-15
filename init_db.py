from aiomysql import create_pool
from config import DBConfig

async def init_db(db_config: DBConfig):
    async with create_pool(
        host=db_config.host,
        port=db_config.port,
        user=db_config.user,
        password=db_config.password,
        db=db_config.database
    ) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Створення бази даних
                await cur.execute(
                    f"CREATE DATABASE IF NOT EXISTS {db_config.database} "
                    f"CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
                )
                await cur.execute(f"USE {db_config.database};")

                # Таблиця категорій
                await cur.execute(""" 
                    CREATE TABLE IF NOT EXISTS categories (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL UNIQUE
                    );
                """)

                # Додавання категорій
                new_categories = [
                    ("Цукерки",), ("Шоколад",), ("Печиво",), ("Мармелад",),
                    ("Желейні ведмедики",), ("Трюфелі",), ("Льодяники",), ("Карамель",),
                    ("Зефір",), ("Пастила",), ("Медові цукерки",), ("Дитячі солодощі",),
                    ("Десерти без цукру",), ("Сезонні солодощі",), ("Торти",),
                    ("Кондитерські прилади",), ("Форми для випічки",),
                ]

                for category in new_categories:
                    await cur.execute("SELECT id FROM categories WHERE name = %s", (category[0],))
                    if not await cur.fetchone():
                        await cur.execute("INSERT INTO categories (name) VALUES (%s)", category)

                # Таблиця товарів
                await cur.execute(""" 
                    CREATE TABLE IF NOT EXISTS products (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        description TEXT,
                        price DECIMAL(10,2),
                        category_id INT,
                        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
                    );
                """)

                # Таблиця замовлень
                await cur.execute(""" 
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id INT AUTO_INCREMENT PRIMARY KEY,
                        product_name VARCHAR(255),
                        quantity INT,
                        customer_name VARCHAR(255),
                        phone_number VARCHAR(20),
                        status VARCHAR(50),
                        user_id BIGINT
                    );
                """)

                # Таблиця користувачів
                await cur.execute(""" 
                    CREATE TABLE IF NOT EXISTS users (
                        user_id BIGINT PRIMARY KEY,
                        username VARCHAR(255) NOT NULL
                    );
                """)

                # Таблиця відгуків
                await cur.execute("""
                    CREATE TABLE IF NOT EXISTS feedback (
                        feedback_id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id BIGINT,
                        feedback_text TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    );
                """)

                # Додавання адміністратора
                await cur.execute("""
                    INSERT IGNORE INTO users (user_id, username) 
                    VALUES (1038982882, 'admin_user');
                """)

                await conn.commit() 