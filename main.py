from telebot.types import Message
from loader import bot
from states import UserState
from telebot.custom_filters import StateFilter
from set_bot_commands import set_commands
from config import BASE_URL, YDICT_KEY, DEFAULT_COMMANDS
import requests
from keyboard import gen_markup

@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.set_state(message.from_user.id, UserState.base, message.chat.id)
    main_menu(message)

@bot.message_handler(commands=['help'])
def help_command(message: Message):
    result = ''
    text = [f"/{command} - {definition}" for command, definition in DEFAULT_COMMANDS]
    for cmd in text:
        result += f'{cmd}\n'
    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['lang', 'lookup'])
def commands_handler(message: Message):
    if message.text == '/lang':
        bot.set_state(message.from_user.id, UserState.lang, message.chat.id)
        set_lang(message)
    elif message.text == '/lookup':
        bot.set_state(message.from_user.id, UserState.lookup, message.chat.id)
        lookup(message)


@bot.message_handler(state=UserState.base)
def main_menu(message: Message):
    bot.send_message(message.chat.id, f'Ola! {message.from_user.full_name}!'
                                      f' Ты находишься в меню бота-словаря.'
                                      f' Доступные команды ты можешь получить, вписав /help')

@bot.message_handler(state=UserState.lang)
def set_lang(message: Message):
    with bot.retrieve_data(message.from_user.id) as data:
        if data.get('user_langs') is None:
            if data.get('first_half') is None:
                bot.send_message(message.chat.id, f'Введите один из доступных языков', reply_markup=gen_markup())
                return
            if data.get('second_half') is None:
                response = requests.get(f'{BASE_URL}/getLangs', params={'key': YDICT_KEY})
                bot.send_message(message.chat.id, f'Выберите направление перевода', reply_markup=gen_markup(chosen_lang=data['first_half'], langs=response.json()))

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.answer_callback_query(call.id)
    bot.set_state(call.from_user.id, UserState.lang, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id) as data:
        if data.get('first_half') is None:
            data['first_half'] = call.data
            bot.send_message(call.message.chat.id,
                             'Отлично, теперь выберите направление перевода, повторно введя /lang')
        else:
            data['second_half'] = call.data
            data['user_langs'] = f'{data['first_half']}-{data['second_half']}'
            bot.send_message(call.message.chat.id,
                             f'Спасибо, данные сохранены, ваше направление перевода - {data['user_langs']}\n'
                             f'Теперь введите команду /lookup для ввода слов')
            bot.set_state(call.message.from_user.id, UserState.base, call.message.chat.id)

@bot.message_handler(state=UserState.lookup)
def lookup(message: Message):
    if message.text == '/lookup':
        bot.send_message(message.chat.id, 'Вы находитесь в меню перевода слов, введите слово и я его переведу')
        with bot.retrieve_data(message.from_user.id) as data:
            if data.get('user_langs') is None:
                bot.send_message(message.chat.id, 'Перед поиском требуется установить направление перевода! Введите команду /lang')
                return
    else:
        with bot.retrieve_data(message.from_user.id) as data:
            if data.get('user_langs') is None:
                bot.send_message(message.chat.id, 'Перед вводом переводимых слов требуется установить направление перевода! Введите команду /lang')
        with bot.retrieve_data(message.from_user.id) as data:
            response = requests.get(f'{BASE_URL}/lookup', params={
                'key': YDICT_KEY,
                'lang': data['user_langs'],
                'text': message.text,
                'ui': 'ru'
            })
            json_response = response.json()
            if not json_response['def']:
                bot.send_message(message.chat.id, 'Перевод не найден.')
            else:
                translations_list = list()
                for index, translate in enumerate(json_response['def'][0]['tr']):
                    translations_list.append(translate['text'])
                    if index == 4:
                        break
                formatted_response = f'{json_response['def'][0]['text']} - {", ".join(translations_list)}'
                bot.send_message(message.chat.id, formatted_response)


if __name__ == '__main__':
    set_commands(bot)
    bot.add_custom_filter(StateFilter(bot))
    bot.infinity_polling()
