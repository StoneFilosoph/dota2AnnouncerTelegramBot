#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import misc
import telebot
from telebot import types
import twitcher


token = misc.token
bot = telebot.TeleBot(token)
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


def send_message(chat_id, text=None):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


@bot.message_handler(content_types=["text"])
def callback():
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text='Ссылка на Twitch', url=twitcher.twitch_url())
    keyboard.add(url_button)
    msg_but = "Нажми на кнопку для просмотра, матча!"
    bot.send_message(misc.CHANNEL_NAME, msg_but, reply_markup=keyboard)








