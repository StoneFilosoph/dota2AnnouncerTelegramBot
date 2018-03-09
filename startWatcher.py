#! /usr/bin/env python
# -*- coding: utf-8 -*-


import sqlite3,time
import datetime, pytz,tools


def connect_db():
    """connect_db database creator

    provide data base creation, or connect to db if it existed.
    view of db wich created
    | id | time               | team1 | percent1 | team2 | percent2 |organization |  status |
     1    2015-05-17 10:00:00   xD       35      GeekFam    65         starladder  announced

    Создает базу данных, если база уже существует в каталоге, подключается к ней.
    :return:
    """
    con = None
    con = sqlite3.connect('dota2lounge.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS DAY ('
                '"id" INTEGER PRIMARY KEY AUTOINCREMENT,'
                '"time" varchar(30),'
                '"team1" varchar(25),'
                '"percent1" int(5),'
                '"team2" varchar(25),'
                '"percent2" int(5),'
                '"organization" varchar(30),'
                '"status" varchar(15));')

    cur.close()
    con.close()


def match_timers():
    """Watching for time and tell us, when matches are started.



    :return:
    """
    utc = pytz.timezone('UTC')
    con = sqlite3.connect('dota2lounge.db')
    cur = con.cursor()
    l = ('announced',)
    cur.execute('SELECT * FROM DAY WHERE status=?', l)
    a = cur.fetchall()
    cur.close()
    con.close()
    matches = []
    for x in a:
        matches.append(x)
    while matches:
        time.sleep(1)
        soon_match = matches[0]
        utc_time = datetime.datetime.now(utc)
        nowtime = utc_time.timestamp()
        soon = soon_match[1]
        if tools.debug == 1:
            print(nowtime)
        if float(nowtime) > (float(soon)+5000):
            matches.remove(matches[0])
            if tools.debug == 1:
                print('этот матч уже стартовал переходим к след матчу')
            if matches:
                soon_match = matches[0]
        else:
            if matches:
                if tools.debug == 1:
                    print('Сейчас: {}'.format(utc_time.strftime('%Y-%m-%d %H:%M:%S')))
                    print('Самый скорый матч {}'.format(soon_match))
                if float(soon_match[1]) < float(utc_time.timestamp()):
                    soon_match_id = soon_match[0]
                    con = sqlite3.connect('dota2lounge.db')
                    cur = con.cursor()
                    l = ('readyToStart', soon_match_id)
                    cur.execute('UPDATE DAY SET status=? WHERE id=?', l)
                    con.commit()
                    cur.close()
                    con.close()
                    matches.remove(matches[0])


    if tools.debug == 1:
        print ('На Сегодня матчи - ВСЁ, до завтра')

    pass


# con = sqlite3.connect('dota2lounge.db')
# cur = con.cursor()
# l = ('announced', 'readyToAnnounce')
# cur.execute('UPDATE DAY SET status=? WHERE status=?', l)
# con.commit()
# cur.close()
# con.close()
def main():
    connect_db()
    while True:
        time.sleep(300)
        match_timers()

if __name__ == '__main__':
    main()

