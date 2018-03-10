#! /usr/bin/env python
# -*- coding: utf-8 -*-


from urllib.request import Request, urlopen
import sqlite3
from bs4 import BeautifulSoup
import time,tools,pytz,datetime



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


def parser_end_watch(html, matches_ended):
    """Parser will parsing your html and return list of macthes







    :param html: give to him html, please
    :return:
    """

    soup = BeautifulSoup(html,'html.parser')
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
                teams_couple.append(team.find('b').text + '-WIN')
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
        total = (a, b, int(c[:-1]), d, int(e[:-1]), f)
        if (b.find('-WIN') > -1) or (d.find('-WIN') > -1):
            matches_ended.append(total)

        counter += 1

    return matches_ended


def end_watcher():
    matches = []
    matches_ended =[]
    utc = pytz.timezone('UTC')
    utc_time = datetime.datetime.now(utc)
    con = sqlite3.connect('dota2lounge.db')
    cur = con.cursor()
    l = ('started',)
    cur.execute('SELECT * FROM DAY  WHERE status=?', l)
    a = cur.fetchall()
    cur.close()
    con.close()
    for x in a:
        matches.append(x)
    parser_end_watch(get_html('https://dota2lounge.com/'), matches_ended)
    if tools.debug == 1:
        print(matches_ended)
        print(matches)
    for x in matches:
        for y in matches_ended:
            utc_time = datetime.datetime.now(utc)
            if ((float(utc_time.timestamp())-float(y[0])) > 1200)and ((float(utc_time.timestamp())-float(y[0])) < 25200) and (x[6] == y[5]) and \
                    ((y[1].find(x[2]) > -1) and (y[1].find('-WIN') > -1)):
                if tools.debug == 1:
                    print('Среди команд {} и {}, победила команда {}'.format(x[2], x[4], x[2]))
                team_winner = 'победила команда '+ x[2]
                l =(team_winner, 'readyToEnd', x[0])
                con = sqlite3.connect('dota2lounge.db')
                cur = con.cursor()
                cur.execute('UPDATE DAY SET time=?, status=? WHERE id=?',l)
                con.commit()
                cur.close()
                con.close()

            if ((float(utc_time.timestamp())-float(y[0])) > 1200)and ((float(utc_time.timestamp())-float(y[0])) < 25200) and (x[6] == y[5]) and \
                    ((y[3].find(x[4]) > -1) and (y[3].find('-WIN') > -1)):
                if tools.debug == 1:
                    print('Среди команд {} и {}, победила команда {}'.format(x[2], x[4], x[4]))
                team_winner = 'победила команда ' + x[4]
                l = (team_winner, 'readyToEnd', x[0])
                con = sqlite3.connect('dota2lounge.db')
                cur = con.cursor()
                cur.execute('UPDATE DAY SET time=?, status=? WHERE id=?', l)
                con.commit()
                cur.close()
                con.close()

            else:
                if tools.debug == 1:
                    print('к следующему матчу')

    pass

def main():
    while True:
        time.sleep(130) #130
        end_watcher()

if __name__ == '__main__':
    main()