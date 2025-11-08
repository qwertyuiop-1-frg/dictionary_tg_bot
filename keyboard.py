from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


language_dict = {
    "de": "Немецкий",
    "nl": "Нидерландский",
    "mhr": "Марийский",
    "cs": "Чешский",
    "lt": "Литовский",
    "it": "Итальянский",
    "mrj": "Горномарийский",
    "ru": "Русский",
    "en": "Английский",
    "tt": "Татарский",
    "sv": "Шведский",
    "et": "Эстонский",
    "sk": "Словацкий",
    "no": "Норвежский",
    "zh": "Китайский",
    "uk": "Украинский",
    "be": "Белорусский",
    "da": "Датский",
    "bg": "Болгарский",
    "el": "Греческий",
    "pl": "Польский",
    "tr": "Турецкий",
    "es": "Испанский",
    "pt": "Португальский",
    "hu": "Венгерский",
    "lv": "Латышский",
    "fr": "Французский",
    "fi": "Финский"
}

inverse_dict = {v: k for k, v in language_dict.items()}

def gen_markup(chosen_lang=None, langs=None):
    keyboard = InlineKeyboardMarkup()
    if chosen_lang is None:
        for lang in inverse_dict.keys():
            button = InlineKeyboardButton(text=lang, callback_data=inverse_dict[lang])
            keyboard.add(button)
    else:
        usr_first_abbr = chosen_lang
        second_half = dict(map(lambda full_abbr: (language_dict[full_abbr.split('-')[1]], full_abbr.split('-')[1]),
                               (filter(lambda lang: lang.startswith(usr_first_abbr), langs))))
        for lang in second_half.keys():
            button = InlineKeyboardButton(text=lang, callback_data=inverse_dict[lang])
            keyboard.add(button)
    return keyboard
