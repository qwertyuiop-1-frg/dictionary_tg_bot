from telebot.types import BotCommand
from loader import bot
from config import DEFAULT_COMMANDS


def set_commands(bot):
    bot.set_my_commands(
        BotCommand(*i) for i in DEFAULT_COMMANDS
    )
