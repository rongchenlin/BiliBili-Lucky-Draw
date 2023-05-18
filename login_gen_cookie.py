import json
from datetime import datetime
from time import sleep
from urllib.parse import urlparse

from selenium.webdriver.common.by import By

from utils.selenium_util import is_xpath_exist, init_webdriver3


def login_manual(bro):
    while is_xpath_exist(bro, '//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div') is True:
        print(datetime.now().strftime("%H:%M:%S") + '：等待扫描登录')
        sleep(1)
    print('登录成功，正在保存cookie')
    dict_cookies = bro.get_cookies()
    json_cookies = json.dumps(dict_cookies)
    sleep(3)
    try:
        url = bro.find_element(By.XPATH, '//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[1]/div[1]/a[1]').get_attribute("href")
    except Exception as e:
        print(e)
    result = urlparse(url)
    id = str(result[2])[1:]
    cookie_path = './' + id + '.txt'
    with open(cookie_path, 'w') as f:
        f.write(json_cookies)
    print('cookies保存成功！')

if __name__ == '__main__':
    homeUrl = 'https://www.bilibili.com/'
    # 初始化
    bro, chains = init_webdriver3()
    bro.get(homeUrl)
    # 登录
    login_manual(bro)
    bro.quit()