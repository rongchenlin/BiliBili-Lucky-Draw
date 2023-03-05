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
import time
import schedule
import requests
import socket
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
    bro = webdriver.Chrome(service=s, chrome_options=chrome_options, options=option)
    # bro = webdriver.Chrome(service=s)
    chains = ActionChains(bro)
    return bro, chains


def login_manual(bro, cookie_path):
    while is_xpath_exist(bro, '//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div') is True:
        print(datetime.now().strftime("%H:%M:%S") + '：等待扫描登录')
        sleep(1)
    print('登录成功，正在保存cookie')
    dict_cookies = bro.get_cookies()
    json_cookies = json.dumps(dict_cookies)
    sleep(1)
    with open(cookie_path, 'w') as f:
        f.write(json_cookies)
    print('cookies保存成功！')


def error_to_log(function_name, content, note):
    try:
        ip = get_host_ip()
        db = init_db('bilibili')
        # 保存记录
        params = {}
        params['function_name'] = function_name
        params['content'] = str(content).replace('"', '').replace("'", '')[:2500]
        params['note'] = note
        params['ip'] = ip
        params['insert_time'] = str(datetime.now())
        db.insert('t_log', params)
    except Exception as e:
        print(e)
    # finally:
    #     # db.close()
    #     print("日志完成入库")


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
        error_to_log("login_by_cookie", "cookie登录失败", "p0")
    # finally:
    #     bro.quit()


def is_xpath_exist(bro, xpath):
    try:
        bro.find_element(By.XPATH, xpath)
        return True
    except:
        return False


def do_share(bro, chains, fans_id, userId):
    try:
        attempt = 0
        success = False
        dyn_id_list = []
        while attempt < 5 and not success:
            try:
                url = 'https://space.bilibili.com/' + fans_id + '/dynamic'
                bro.get(url)
                i = 1
                sleep(10 + attempt * 10)
                share_list = bro.find_elements(By.XPATH, '//*[@id="page-dynamic"]/div[1]/div/div[1]/*/div/div')
                print("share_list")
                print(fans_id)
                print(share_list)
                for x in share_list:
                    time = x.find_element(By.XPATH, './div[2]/div[2]').text
                    if "小时" in time or "分钟" in time or "刚刚" in time or "昨天" in time:
                        # 判断是否互动抽奖
                        is_draw_name = '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' + str(
                            i) + ']/div/div/div[3]/div/div[2]/div[2]/div/div[1]/span[2]'
                        if is_xpath_exist(bro, is_draw_name) is False:
                            continue
                        dyn_id = x.find_element(By.XPATH,
                                                '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' + str(
                                                    i) + ']/div/div/div[3]/div/div[2]/div[3]/div').get_attribute(
                            "dyn-id")
                        # 保存所有的要转发的ID
                        dyn_id_list.append(dyn_id)
                    i = i + 1
                success = True
            except Exception as e1:
                attempt = attempt + 1
                print("寻找转发列表重试中。。。")
                sleep(2)
                if attempt == 5:
                    error_to_log("start_forward", "转发动态[寻找转发列表]出错：" + repr(type(e1)), "p1")
                    break


        db = init_db('bilibili')
        print(dyn_id_list)
        for dyn_id in dyn_id_list:
            attempt = 0
            success = False
            while attempt < 3 and not success:
                try:
                    # 如果是已经转发过的，跳过，不转发
                    sql = "SELECT * FROM t_share where dyn_id  = " + dyn_id  # sql语句，可自行对应自己数据相应的表进行操作
                    data = db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
                    if len(data) != 0:
                        break

                    new_url = 'https://t.bilibili.com/' + dyn_id
                    bro.get(new_url)
                    sleep(12)

                    # 移动到头像
                    touxiang = bro.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div')
                    sleep(1)
                    chains.move_to_element(touxiang).perform()
                    sleep(1)

                    # 点击关注
                    follow = bro.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[3]/div[1]')
                    follow_text = follow.get_attribute('innerText')
                    sleep(1)
                    if "已关注" not in follow_text:
                        chains.click(follow).perform()

                    sleep(1)
                    share_btn = bro.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div/div[1]/div[4]/div[1]/div/i')
                    sleep(1)
                    chains.click(share_btn).perform()
                    sleep(1)
                    do_share_btn = bro.find_element(By.XPATH,
                                                    '//*[@id="app"]/div[2]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/div['
                                                    '2]/button')
                    sleep(1)
                    chains.click(do_share_btn).perform()
                    sleep(1)

                    # 保存记录
                    params = {}
                    params['user_id'] = userId
                    params['fans_id'] = fans_id
                    params['dyn_id'] = dyn_id
                    params['flag'] = str(1)
                    params['insert_time'] = str(datetime.now())
                    db.insert('t_share', params)
                    success = True
                except Exception as e2:
                    attempt = attempt + 1
                    sleep(10)
                    if attempt == 3:
                        error_to_log("start_forward", "转发动态[执行转发or入库]出错：" + repr(type(e2)), "p1")
                        break
    except Exception as e3:
        print(e3)
        # error_to_log("start_forward", "转发动态出错：" + repr(type(e3)), "p1")


def get_fans_id_list(bro, chains, user_id):
    try:
        url = 'https://space.bilibili.com/' + user_id + '/fans/follow'
        bro.get(url)
        sleep(1)
        nums = bro.find_element(By.XPATH, '//*[@id="n-gz"]').text
        next_xpath = '//*[@id="page-follows"]/div/div[2]/div[2]/div[2]/ul[2]/li[7]/a'
        user_url_list = []
        i = 0
        while i < 20:
            xpath = '//*[@id="page-follows"]/div/div[2]/div[2]/div[2]/ul[1]/li[' + str(i % 20 + 1) + ']/a'
            i = i + 1
            if is_xpath_exist(bro, xpath) is True:
                url = bro.find_element(By.XPATH, xpath).get_attribute('href')
                user_url_list.append(url)

        if int(nums) > 20:
            i = 0
            while is_xpath_exist(bro, next_xpath) is True:
                next_btn = bro.find_element(By.XPATH, next_xpath)
                chains.click(next_btn).perform()
                sleep(1)
                xpath = '//*[@id="page-follows"]/div/div[2]/div[2]/div[2]/ul[1]/li[' + str(i % 20 + 1) + ']/a'
                i = i + 1
                if is_xpath_exist(bro, xpath) is True:
                    url = bro.find_element(By.XPATH, xpath).get_attribute('href')
                    user_url_list.append(url)
        print(user_url_list)
        return user_url_list
    except Exception as e1:
        print(e1)


def remove_share(bro, chains, user_id):
    url = 'https://space.bilibili.com/' + user_id + '/dynamic'
    bro.get(url)
    sleep(1)
    share_list = bro.find_elements(By.XPATH, '//*[@id="page-dynamic"]/div[1]/div/div[1]/*/div/div')
    for x in share_list:
        time = x.find_element(By.XPATH, './div[2]/div[2]').text
        # if "小时" in time or "分钟" in time or "刚刚" in time:
        if 1 == 1:

            pre_delete_btn = x.find_element(By.XPATH,
                                            '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[1]/div/div/div[2]/div[4]/div')
            chains.click(pre_delete_btn).perform()
            sleep(random.randint(1, 5))
            delete_btn = x.find_element(By.XPATH,
                                        '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[1]/div/div/div[2]/div[4]/div/div/div[2]/div[2]')
            try:
                chains.click(delete_btn).perform()
            except Exception as e:
                print(repr(e))
            sleep(random.randint(1, 5))
            try:
                do_delete_btn = x.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[3]/button[1]')
                chains.click(do_delete_btn).perform()
            except Exception as e:
                print(repr(e))
            sleep(random.randint(1, 5))
    print(user_id + ' 完成删除过期动态!')


def init_db(db_name):
    config = {
        'host': '123.56.224.232',
        'port': 3306,
        'user': 'bilibili',
        'passwd': 'bilibili',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor
    }
    db = mysql_operate.MysqldbHelper(config)
    db.selectDataBase(db_name)
    return db


def get_fans_list():
    try:
        db = init_db('bilibili')
        sql = "SELECT * FROM t_fans;"
        data = db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
        list = []
        for fans in data:
            list.append(fans['fans_id'])
        return list
    except Exception as e1:
        print(e1)


def start_forward():
    try:
        print('[Start]开始动态转发，当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        # 初始化打开数据库连接
        db = init_db('bilibili')
        userId = '433441242'
        # userId = '385649497'
        cookie_path = './' + userId + '.txt'
        homeUrl = 'https://www.bilibili.com/'
        # 初始化
        bro, chains = init_webdriver()
        bro.get(homeUrl)

        # 登录
        # login_manual(bro, cookie_path)
        login_by_cookie(bro, cookie_path)

        # 获取用户ID列表
        ids_list = get_fans_list()

        # 执行转发操作
        i = 1
        for id in ids_list:
            do_share(bro, chains, id, userId)
            sleep(2)
            print("第 " + str(i) + "个用户, id = " + id + ' 转发完成!')
            i = i + 1

        # 删除过期动态
        # remove_share(bro, chains, userId)
    except Exception as e2:
        error_to_log("start_forward", "转发动态出错：" + repr(type(e2)), "p1")
    finally:
        print('[Finish]结束动态转发，当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        bro.quit()


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def send_start_forward():
    try:
        print('开始转发')
        url1 = 'https://sctapi.ftqq.com/SCT172323TZn2oLYosf0TJY80XSH7KN29R.send'
        url2 = 'https://sctapi.ftqq.com/SCT63874Tus7GmUoMlz6b2iJNxrQ1gUws.send'
        data = {
            'title': 'Start 开始转发',
            'desp': 'Start 开始转发',
            'short': 'Start 开始转发'
        }
        r = requests.post(url1, data)
        r = requests.post(url2, data)
    except Exception as e2:
        error_to_log("send_start_forward", "筛选任务开始发送通知出错：" + repr(type(e2)), "无")


if __name__ == '__main__':

    start_forward()
    print("start main task")
    schedule.every().day.at("11:00").do(start_forward)
    schedule.every().day.at("21:00").do(start_forward)
    schedule.every().day.at("21:10").do(send_start_forward)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            time.sleep(1)
            print(e)
