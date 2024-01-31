import json
from time import sleep
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from service.log_service.log_printer_service import MyLogger
from utils import globals
from utils.file_util import append_data_to_env
from utils.time_util import random_sleep
from utils.webdriver_util import ElementUtil, init_webdriver

mylogger = MyLogger('login_service.py').getLogger()


class LoginService(object):
    def __init__(self, bro, chains, my_user_id='0'):
        self.bro = bro
        self.chains = chains
        self.my_user_id = my_user_id
        mylogger.error('启动登录模块')

    def login_manual(self):
        self.bro.get(globals.home_url)
        while ElementUtil.is_xpath_exist(self.bro, self.chains,
                                         '//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div') is True:
            random_sleep()
        dict_cookies = self.bro.get_cookies()
        json_cookies = json.dumps(dict_cookies)
        try:
            url = self.bro.find_element(By.XPATH,
                                        '//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[1]/div[1]/a[1]').get_attribute(
                "href")
        except Exception as e:
            print(e)
        result = urlparse(url)
        id = str(result[2])[1:]
        cookie_path = './cookie/' + id + '.txt'
        with open(cookie_path, 'w') as f:
            f.write(json_cookies)

    def login_by_cookie(self):
        """
        根据保存的Cookie信息进行登录
        :param bro:
        :return:
        """
        try:
            self.bro.get(globals.home_url)
            cookie_value = globals.cookie_value
            cookie = {"domain": ".bilibili.com", "expiry": 1717635533, "name": "SESSDATA", "path": "/", "sameSite": "Lax", "value": cookie_value}
            self.bro.add_cookie(cookie)
            self.bro.refresh()
            mylogger.error('使用cookie自动登录成功！')
            random_sleep(start=1, end=2)
        except Exception as e:
            mylogger.error('登录失败')
            mylogger.error("[出错原因为：%s]" % e)

    def login_by_cookie2(self):
        """
        根据保存的Cookie信息进行登录
        :param bro:
        :return:
        """
        try:
            cookie_path = './cookie/' + self.my_user_id + '.txt'
            self.bro.get(globals.home_url)
            with open(cookie_path, 'r', encoding='utf-8') as f:
                cookies = f.readlines()
            for cookie in cookies:
                cookie = cookie.replace(r'\n', '')
                cookie_li = json.loads(cookie)
                random_sleep(start=1, end=2)
                for cookie in cookie_li:
                    self.bro.add_cookie(cookie)
                self.bro.refresh()
            mylogger.error('使用cookie自动登录成功！')
            random_sleep(start=1, end=2)
        except Exception as e:
            mylogger.error('登录失败')
            mylogger.error("[出错原因为：%s]" % e)
