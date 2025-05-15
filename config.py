from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class DBConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

@dataclass
class Config:
    bot_token: str
    db: str
    db_config: DBConfig

    @staticmethod
    def create():
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD", "")
        db_host = os.getenv("DB_HOST")
        db_port = int(os.getenv("DB_PORT"))
        db_name = os.getenv("DB_NAME")
        bot_token = os.getenv("BOT_TOKEN")

        db_uri = f"mysql+aiomysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        db_config = DBConfig(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )

        return Config(bot_token=bot_token, db=db_uri, db_config=db_config)

config = Config.create()






