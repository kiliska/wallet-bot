import telebot
from telebot import types

from config import *
from extension import Converter
from extension import APIException


def create_markup(base = None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button = []
    for val in keys.keys():
        if val != base:
            button.append(types.KeyboardButton(val.capitalize()))

    markup.add(*button)
    return markup

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Приветствую! Для конвертации используй команду /convert'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберете валюту, из которой конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=create_markup())
    bot.register_next_step_handler(message, quote_handler)


def quote_handler(message: telebot.types.Message):
    quote = message.text.strip().lower()
    text = 'Выберете валюту, в которую конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=create_markup(quote))
    bot.register_next_step_handler(message, base_handler, quote)


def base_handler(message: telebot.types.Message, quote):
    base = message.text.strip()
    text = 'Введите количество конвертируемой валюты: '
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, quote, base)


def amount_handler(message: telebot.types.Message, quote, base):
    amount = message.text.strip()
    try:
        new_price = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации: \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} : {new_price}'
        bot.send_message(message.chat.id, text)


while True:
    try:
        bot.polling()
    except:
        continue