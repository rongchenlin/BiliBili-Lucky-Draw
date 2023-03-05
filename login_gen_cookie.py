import random
from datetime import datetime
from selenium import webdriver
from lxml import etree
from time import sleep
# 实现无可视化界面
from selenium.webdriver.chrome.options import Options
# 实现规避检测
from selenium.webdriver import ChromeOptions
import json
from urllib.parse import urlparse

import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import mysql_operate


def init_webdriver():
    # # 实现无可视化界面的操作
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 实现规避检测的变量：option
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 实现让selenium规避被检测到的风险

    s = Service(r"./chromedriver.exe")
    # bro = webdriver.Chrome(service=s, chrome_options=chrome_options, options=option)
    bro = webdriver.Chrome(service=s)
    chains = ActionChains(bro)
    return bro, chains

def is_xpath_exist(bro, xpath):
    try:
        bro.find_element(By.XPATH, xpath)
        return True
    except:
        return False


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
    bro, chains = init_webdriver()
    bro.get(homeUrl)
    # 登录
    login_manual(bro)
    bro.quit()