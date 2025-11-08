from telebot.states import State, StatesGroup

class UserState(StatesGroup):
    base = State()
    lang = State()
    lookup = State()
