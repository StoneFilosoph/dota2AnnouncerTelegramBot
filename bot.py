#! /usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import misc



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
