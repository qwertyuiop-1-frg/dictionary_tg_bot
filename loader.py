from telebot import TeleBot, StateMemoryStorage
from config import BOT_TOKEN

storage = StateMemoryStorage()
bot = TeleBot(token=BOT_TOKEN, state_storage=storage)
