#! /usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import misc
import json
import sqlite3


def connect_db2():
    """connect_db database creator

    provide data base creation, or connect to db if it existed.
    view of db wich created
    | id | time               | team1 | percent1 | team2 | percent2 |
     1    2015-05-17 10:00:00   xD       35      GeekFam    65

    :return: 
    """
    con = None
    con = sqlite3.connect('dota2lounge.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS USERS ('
                '"id" INTEGER PRIMARY KEY AUTOINCREMENT,'
                '"chat_id" varchar(30));')


def clear_base():

    """Очистить базу
    clear_base()"""

    con = None
    con = sqlite3.connect('USERS.db')
    cur = con.cursor()
    cur.execute('DELETE FROM USERS')
    var = cur.fetchall()
    print(var)
    con.commit()
    cur.close()
    con.close()


token = misc.token

URL = 'https://api.telegram.org/bot' + token + '/'

#  https://api.telegram.org/bot358083147:AAEXO9i1VbhQZj3VdPu88PLYx1rnHG-efOE/sendmessage?chat_id=403555014&text=Hi


def get_updates():

    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()


def get_message():

    data = get_updates()
    chat_id = data['result'][-1]['message']['chat']['id']
    message_text = data['result'][-1]['message']['text']
    message = {'chat_id': chat_id, 'text': message_text}


    chat_id_cor = (chat_id,)


    print(chat_id_cor)
    print(message_text)
    print(data)
    print(message)

    if message_text == '/start':
        connect_db2()
        con = sqlite3.connect('dota2lounge.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM USERS WHERE chat_id LIKE {}'.format(chat_id))
        var = cur.fetchall()
        cur.close()
        con.close()

        if var == []:
            connect_db2()
            print('вход в базу..')
            con = sqlite3.connect('dota2lounge.db')
            cur = con.cursor()
            cur.execute('INSERT INTO USERS(chat_id) VALUES (?)', chat_id_cor)
            con.commit()
            cur.close()
            con.close()

        connect_db2()
        con = sqlite3.connect('dota2lounge.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM USERS')
        var = cur.fetchall()

        print(var)
        cur.close()
        con.close()

    return message


def send_message(chat_id, text = 'Wait a second,please...'):

    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


def main():

    d = get_updates()
    with open('updates.json', 'w')as file:
        json.dump(d, file, indent = 2, ensure_ascii = False)

    # answer = get_message()
    # chat_id = answer['chat_id']
    # con = sqlite3.connect('USERS.db')
    # cur = con.cursor()
    # cur.execute('SELECT * FROM USERS')
    # var = cur.fetchall()
    #
    # for x in var:
    #     send_message(x[1],)

if __name__ == '__main__':

    main()
