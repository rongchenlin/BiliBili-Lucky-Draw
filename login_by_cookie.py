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

def login_by_cookie(bro, cookie_path):
    try:
        with open(cookie_path, 'r', encoding='utf-8') as f:
            cookies = f.readlines()
        for cookie in cookies:
            cookie = cookie.replace(r'\n', '')
            cookie_li = json.loads(cookie)
            sleep(1)
            for cookie in cookie_li:
                bro.add_cookie(cookie)
            bro.refresh()
        print('使用cookie自动登录成功！')
        sleep(1)
    except Exception as e:
        print(e)
        print('登录失败')


if __name__ == '__main__':
    homeUrl = 'https://www.bilibili.com/'
    # 初始化
    bro, chains = init_webdriver()
    bro.get(homeUrl)
    # 登录
    userId = '433441242'
    # userId = '385649497'
    cookie_path = './' + userId + '.txt'
    login_by_cookie(bro, cookie_path)
    input()
    bro.quit()