from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sqlite3, time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_path = 'C:\\Users\Mahindr\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\selenium\webdriver\chromedriver_win32\chromedriver.exe'


def twitch_url():

    # time.sleep(60)
    # while True:

        con = sqlite3.connect('dota2lounge.db')
        cur = con.cursor()
        rts = ('readyToStart',)
        cur.execute('SELECT * FROM DAY WHERE (status = ?)', rts)
        a = cur.fetchall()
        matches = []
        for x in a:
            matches.append(x)
        for x in matches:
            res = '{}'.format(x[6])

            driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)
            driver.get("https://www.twitch.tv")

            search_form = driver.find_element_by_id('nav-search-input')
            search_form.click()
            search_form.send_keys(res)
            time.sleep(2)
            file = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/nav/div/div[1]/div[2]/div/div/div/div[2]/div/div/div/div[2]/div[3]/div/div/div[1]/div[2]/div/div/div[1]')
            file.click()
            time.sleep(1)
            url = driver.current_url
            driver.quit()
            return url


