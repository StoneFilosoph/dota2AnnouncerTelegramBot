#! /usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sqlite3, time
import datetime, pytz,tools


def connect_db():
    """connect_db database creator

    provide data base creation, or connect to db if it existed.
    view of created db table
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


def get_html(url):
    """Get html

    Just give him url of dota2lounge, its will not working other way
    Просто передавайте этой функции УРЛ дота2лоунжа и она будет довольна.

    :param url: dota2loungeUrl
    :return: html
    """
    url_request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    response = urlopen(url_request)
    return response.read()


def parser_start_day(html):
    """Parser will parsing your html and write some things to db

    At start of the day, it will parse html he got. 
    Trying to separate matches. 


    В начале дня пытается искать предстоящие на сегодня матчи 


    :param html: give to him html, please
    :return: 
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('article', id='bets')
    match_time = []
    teams_couple = []
    teams_percents = []
    organization = []
    con = None
    con = sqlite3.connect('dota2lounge.db')
    cur = con.cursor()
    for row in table.find_all('div', class_='matchmain'):
        match_time.append(row.find('span', class_='match-time').text)
        organization.append(row.find('div', class_='eventm').text)

        for team in row.find_all('div', class_='teamtext'):
            if team.parent.find('img', src='//dota2lounge.com/img/won.png'):
                teams_couple.append(team.find('b').text + '-ALREADYEND')
            else:
                teams_couple.append(team.find('b').text)
            teams_percents.append(team.find('i', class_='percent-coins').text)


            # print(team.find('b').text)
            # print(team.find('i', class_='percent-coins').text)
    number_of_matches = len(match_time)
    counter = 0
    total = ()

    while counter != number_of_matches:

        a = tools.unix_timestamp(match_time[counter],'Etc/GMT-2')
        b = teams_couple[counter * 2]
        c = teams_percents[counter * 2]
        d = teams_couple[counter * 2 + 1]
        e = teams_percents[counter * 2 + 1]
        f = organization[counter]
        g = 'readyToAnnounce'
        total = (a, b, int(c[:-1]), d, int(e[:-1]), f, g)
        pre_total = (a, b, d)
        cur.execute('SELECT * FROM DAY WHERE (time = ? and team1 = ? and team2 = ?)', pre_total)
        a = cur.fetchall()
        if tools.debug == 1:
            print(a)
        if not a:
            cur.execute(
                'INSERT INTO DAY (time, team1, percent1, team2, percent2, organization, status) VALUES (?,?,?,?,?,?,?)', total)
            if tools.debug == 1:
                print('записал')
        else:
            if tools.debug == 1:
                print('одинаково')

        counter += 1

    pass
    con.commit()
    cur.close()
    con.close()


def new_day_grab():
    """works only once at day

    delete already ended matches and mathes already started
    all other matches will be push to the base

    :return:
    """
    utc = pytz.timezone('UTC')
    utc_time = datetime.datetime.now(utc)
    connect_db()
    parser_start_day(get_html('https://dota2lounge.com/'))
    expression = ('%-ALREADYEND', '%-ALREADYEND')
    con = None
    con = sqlite3.connect('dota2lounge.db')
    cur = con.cursor()
    cur.execute('DELETE FROM DAY WHERE team1 LIKE ? or team2 LIKE ?', expression)
    con.commit()
    cur.execute('SELECT * FROM DAY')
    a = cur.fetchall()
    for x in a:
        b = x[1]
        if float(b) < float(utc_time.timestamp()):
            l = (x[0],)
            cur.execute('DELETE FROM DAY WHERE id=?', l)
            con.commit()
    cur.close()
    con.close()


def main():
    msk = pytz.timezone('Europe/Moscow')
    while True:
        msk_time = datetime.datetime.now(msk)
        if msk_time.strftime('%H:%M:%S') == '09:00:00':
            new_day_grab()


if __name__ == '__main__':
    main()