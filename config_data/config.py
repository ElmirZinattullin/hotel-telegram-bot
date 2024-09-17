import os
from dotenv import load_dotenv, find_dotenv
from database import config_db

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()
    config_db.create_bd()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("help", "Вывести справку"),
    ("main_menu", "Вернуться в главное меню"),
    ("back", "Назад"),
    # ("history", "История запросов"),
    ("stop", "Остановить бота")
)
