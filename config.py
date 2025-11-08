import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
YDICT_KEY = os.getenv('YDICT_KEY')
DEFAULT_COMMANDS = (
    ('start', 'Главное меню'),
    ('help', 'Список команд'),
    ('lang', 'Выбор языка'),
    ('lookup', 'Поиск слова или фразы')
)
BASE_URL = 'https://dictionary.yandex.net/api/v1/dicservice.json'