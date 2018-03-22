#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import misc
import telebot
from telebot import types


bot = telebot.TeleBot(misc.token)
token = misc.token
URL = 'https://api.telegram.org/bot' + token + '/'


def get_updates():

    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()


def get_message():

    data = get_updates()
    chat_id = data['result'][-1]['message']['chat']['id']
    message_text = data['result'][-1]['message']['text']
    message = {'chat_id': chat_id, 'text': message_text}

    return message


def send_message(chat_id, text = 'Wait a second,please...'):

    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


# Обработчик команд '/start' и '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    pass

 # Обработчик для документов и аудиофайлов
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass


 #Обработчик сообщений, подходящих под указанное регулярное выражение
@bot.message_handler(regexp="SOME_REGEXP")
def handle_message(message):
    pass


 # Обработчик сообщений, содержащих документ с mime_type 'text/plain' (обычный текст)
@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def handle_text_doc(message):
    pass


@bot.message_handler(content_types=["text"])
def default_test():
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Cсылка на Twitch", url="https://www.twitch.tv/")
    keyboard.add(url_button)
    bot.send_message(misc.CHANNEL_NAME, "Можешь нажать на кнопку и посмотреть прямо сейчас!", reply_markup=keyboard)
    pass




