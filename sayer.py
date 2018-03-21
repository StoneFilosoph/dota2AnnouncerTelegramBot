#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3,time
import misc,tools
import bot


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


def readyToAnnounce():

    con = sqlite3.connect('dota2lounge.db')
    cur = con.cursor()
    l = ('readyToAnnounce',)
    cur.execute('SELECT * FROM DAY WHERE (status = ?)', l)
    a = cur.fetchall()
    matches = []
    result = ""
    org = ""
    for x in a:
        matches.append(x)
        res = matches[-1]
        team_1 = str(res[2])
        teamredact1 = (''.join(str(team_1)for team_1 in team_1))
        team_2 = str(res[4])
        teamredact2 = (''.join(str(team_1) for team_1 in team_2))
        times = str(res[1])
        orgn = str(res[6])

        t = (tools.zone_from_timestamp(times, 'Etc/GMT-3'))
        t2 = (t[10:-3])

        result = result + "В{} играют команды:" \
                          " \n|{}|--- VS ---|{}|\nTournament: {}\n\n".format(t2, teamredact1, teamredact2, orgn)

    if a == []:
        if tools.debug == 1:
            print('1. Ничего не отправлено, нет матчей в статусе readyToAnnounce', result)

    else:
        bot.send_message(misc.CHANNEL_NAME, "Составляем список матчей на сегодня...")
        time.sleep(2)
        bot.send_message(misc.CHANNEL_NAME, org)
        time.sleep(1)
        bot.send_message(misc.CHANNEL_NAME, result)
        if tools.debug == 1:
            print("1. Отправлено в канал, все матчи на сегодня:\n", result)

    cur.close()
    con.close()


def announced():

    con = sqlite3.connect('dota2lounge.db')
    cur = con.cursor()
    anon = ('announced',)
    cur.execute('SELECT * FROM DAY WHERE (status = ?)', anon)
    a = cur.fetchall()
    matches = []
    for x in a:
        matches.append(x)
    if tools.debug == 1:
        print("2. Матчи в статусе announced:", matches)

    cur.close()
    con.close()


"""StartWatcher переводит мачти в readyToStart"""


def ready_to_start():

    con = sqlite3.connect('dota2lounge.db')
    cur = con.cursor()
    rts = ('readyToStart',)
    cur.execute('SELECT * FROM DAY WHERE (status = ?)', rts)
    a = cur.fetchall()
    matches = []
    for x in a:
        matches.append(x)
    if tools.debug == 1:
        print("3. Отправлено в канал, начинаются матчи(readyToStart):", matches)

    for x in a:
        bot.send_message(misc.CHANNEL_NAME, "Начинается матч между {} и {}, вы можете его посмотреть прямо сейчас!".format(x[2], x[4]))

    cur.close()
    con.close()


def started():

    con = sqlite3.connect('dota2lounge.db')
    cur = con.cursor()
    anon = ('started',)
    cur.execute('SELECT * FROM DAY WHERE (status = ?)', anon)
    a = cur.fetchall()
    matches = []
    for x in a:
        matches.append(x)
    if tools.debug == 1:
        print("4. Матчи в статусе started:", matches)

    cur.close()
    con.close()


"""еnd Watcher переводит матчи started в readyToEnd и добавляет Win к победившим командам"""


def ready_to_end():

    con = sqlite3.connect('dota2lounge.db')
    cur = con.cursor()
    S = ('readyToEnd',)
    cur.execute('SELECT * FROM DAY  WHERE status=?', S)
    a = cur.fetchall()
    matches_ended = []
    for x in a:
        matches_ended.append(x)
    if tools.debug == 1:
        print("5. Результаты игры отправлены в канал:", matches_ended)

    for x in a:
        bot.send_message(misc.CHANNEL_NAME, "Среди команд {} и {}, {}".format(x[2], x[4], x[1]))

    pass

    cur.close()
    con.close()


def updater():

    connect_db()
    con = sqlite3.connect('dota2lounge.db')
    cur = con.cursor()
    rta = ('readyToAnnounce',)
    cur.execute('SELECT * FROM DAY  WHERE status=?', rta)
    a = cur.fetchall()
    matches_ended = []
    if a == []:
        if tools.debug == 1:
            print("6. Нет матчей, readyToAnnounce - статус не меняем:", matches_ended)

    else:
        for x in a:
            matches_ended.append(x)
        if tools.debug == 1:
            print("6. Смена статуса на announced:", matches_ended)
        sql = """ UPDATE DAY SET status = 'announced' WHERE status = 'readyToAnnounce' """
        cur.execute(sql)

    cur = con.cursor()
    rts = ('readyToStart',)
    cur.execute('SELECT * FROM DAY  WHERE status=?', rts)
    a = cur.fetchall()
    matches_ended = []
    if a == []:
        if tools.debug == 1:
            print("7. Нет матчей, readyToStart - статус не меняем:", matches_ended)
    else:
        for x in a:
            matches_ended.append(x)
        if tools.debug == 1:
            print("7. Смена статуса на started:", matches_ended)
        sql = """ UPDATE DAY SET status = 'started' WHERE status = 'readyToStart' """
        cur.execute(sql)

    cur = con.cursor()
    rte = ('readyToEnd',)
    cur.execute('SELECT * FROM DAY  WHERE status=?', rte)
    a = cur.fetchall()
    matches_ended = []
    if a == []:
        if tools.debug == 1:
            print("8. Нет матчей, readyToEnd - статус не меняем:", matches_ended)
    else:
        for x in a:
            matches_ended.append(x)
        if tools.debug == 1:
            print("8. Смена статуса на end:", matches_ended)
        sql = """ UPDATE DAY SET status = 'end' WHERE status = 'readyToEnd' """
        cur.execute(sql)

    con.commit()
    cur.close()
    con.close()


def del_matches_end():

    con = sqlite3.connect('dota2lounge.db')
    cur = con.cursor()
    end = ('end',)
    cur.execute('SELECT * FROM DAY  WHERE status=?', end)
    a = cur.fetchall()
    matches_ended = []
    if a == []:
        if tools.debug == 1:
            print("9. Нет матчей на удаление из базы:", matches_ended)

    else:
        for x in a:
            matches_ended.append(x)
        if tools.debug == 1:
            print("9. Удаление из базы прошедших матчей:", matches_ended)
        time.sleep(1)
        sql = """ DELETE FROM DAY WHERE status = 'end' """
        cur.execute(sql)
    con.commit()
    cur.close()
    con.close()


def main():

    while True:

        time.sleep(212)
        readyToAnnounce()
        announced()
        ready_to_start()
        started()
        ready_to_end()
        updater()
        del_matches_end()
        if tools.debug == 1:
            print("______________________________________________________________________________________________цикл")

        continue


if __name__ == '__main__':

    main()










