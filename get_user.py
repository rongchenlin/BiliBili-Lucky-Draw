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
import socket

import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import mysql_operate
import requests
from cron_lite import cron_task, start_all
import time
import schedule
# 引入 datetime 模块
import datetime


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


def is_xpath_exist(bro, xpath):
    try:
        bro.find_element(By.XPATH, xpath)
        return True
    except:
        return False


def is_time_ok(time):
    # if "小时" in time or "分钟" in time or "刚刚" in time or "昨天" in time:
    #     return True
    return True;


def check_user(bro, chains, fans_id):
    try:
        db = init_db('bilibili')
        url = 'https://space.bilibili.com/' + fans_id + '/dynamic'
        bro.get(url)
        sleep(2)
        share_list = bro.find_elements(By.XPATH, '//*[@id="page-dynamic"]/div[1]/div/div[1]/*/div/div')
        i = 1
        draw_cnt = 0
        for x in share_list:
            try:
                time = x.find_element(By.XPATH, './div[2]/div[2]').text
                if is_time_ok(time) is True:
                    # 判断是否互动抽奖
                    is_draw_name = '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' + str(
                        i) + ']/div/div/div[3]/div/div[2]/div[2]/div/div[1]/span[2]'
                    if is_xpath_exist(bro, is_draw_name) is True:
                        draw_cnt = draw_cnt + 1
                        last_draw_time = time

            except Exception as e2:
                error_to_log("check_user", "每小时扫描用户程序[判断是否互动抽奖]出错：" + repr(type(e2)), "p3")
                continue
            i = i + 1
        print(draw_cnt)
        if draw_cnt >= 2:
            try:
                # 保存记录
                params = {}
                params['user_id'] = fans_id
                params['draw_cnt'] = str(draw_cnt)
                params['last_time'] = time
                params['last_draw_time'] = last_draw_time
                params['insert_time'] = str(datetime.datetime.now())
                db.insert('t_users_cnt', params)
            except Exception as e3:
                error_to_log("check_user", "每小时扫描用户程序[消息入口]出错：" + repr(type(e3)), "p3")
        sleep(2)
    except Exception as e:
        error_to_log("check_user", "每小时扫描用户程序出错：" + repr(type(e)), "p3")
    # finally:
    #     # db.close()
    #     bro.quit()


def init_db(db_name):
    config = {
        'host': '123.XX.XX.232',
        'port': 3306,
        'user': 'bilibili',
        'passwd': 'XXXXXX',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor
    }
    db = mysql_operate.MysqldbHelper(config)
    db.selectDataBase(db_name)
    return db


def select_user_by_hour():
    try:
        # 初始化打开数据库连接
        print('开始筛选，当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        db = init_db('bilibili')
        sql = "SELECT * FROM t_users_cnt order by insert_time desc "  # sql语句，可自行对应自己数据相应的表进行操作
        data = db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
        max_id = int(data[0]['user_id'])
        # 初始化
        bro, chains = init_webdriver()
        start_id = max_id

        # 执行转发操作
        for i in range(1, 400):
            id = str(start_id + i)
            check_user(bro, chains, id)
            print("No: " + str(i) + ", userId = " + id + ' 扫描完成!')
    except Exception as e:
        error_to_log("select_user_by_hour", "每小时扫描用户程序出错：" + repr(type(e)), "p3")
    finally:
        bro.quit()
        db.close()
        print('结束筛选，当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))


def send_search_start():
    try:
        print('开始筛选')
        url1 = 'https://sctapi.ftqq.com/SCT172323TZn2oLYosf0TJY80XSH7KN29R.send'
        url2 = 'https://sctapi.ftqq.com/SCT63874Tus7GmUoMlz6b2iJNxrQ1gUws.send'
        data = {
            'title': 'Start 筛选用户 定时任务开始',
            'desp': 'Start 筛选用户 定时任务开始',
            'short': 'Start 筛选用户 定时任务开始'
        }
        r = requests.post(url1, data)
        r = requests.post(url2, data)
    except Exception as e:
        error_to_log("send_search_start", "筛选任务开始发送通知出错：" + repr(type(e)), "无")


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday


def deal_time(sj):
    if "小时" in sj or "分钟" in sj or "刚刚" in sj:
        return time.strftime("%Y-%m-%d", time.localtime(time.time()))

    if len(sj) == 5:
        return '2023-' + sj

    return sj;


def search_user():
    try:
        db = init_db('bilibili')
        dayAgo = (datetime.datetime.now() - datetime.timedelta(days=100))
        # 转换为其他字符串格式
        dayAgo = dayAgo.strftime("%Y-%m-%d")
        sql = "SELECT * FROM `t_users_cnt` where TO_DAYS( NOW()) - TO_DAYS(insert_time) =1;"  # sql语句，可自行对应自己数据相应的表进行操作
        list = db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
        print(list)
        for data in list:
            try:
                d_time = data['last_draw_time']
                d_time = deal_time(d_time)
                if d_time >= dayAgo:
                    sql2 = "SELECT * FROM t_fans where fans_id  = " + data['user_id']  # sql语句，可自行对应自己数据相应的表进行操作
                    data2 = db.select_db(sql2)  # 用mysql_operate文件中的db的select_db方法进行查询
                    if len(data2) != 0:
                        continue
                    # 保存记录
                    params = {}
                    params['fans_id'] = data['user_id']
                    params['flag'] = str(data['draw_cnt'])
                    params['insert_time'] = str(datetime.datetime.now())
                    params['update_time'] = d_time
                    db.insert('t_fans', params)
            except Exception as e:
                print(e)
                continue
    except Exception as e2:
        error_to_log("search_user", "二级筛选用户出错：" + repr(type(e2)), "无")
    # finally:
    #     db.close()


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
        params['insert_time'] = str(datetime.datetime.now())
        db.insert('t_log', params)
    except Exception as e:
        print(e)
    finally:
        print("日志完成入库")


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


if __name__ == '__main__':
    print("start search users task")
    schedule.every().day.at("07:30").do(search_user)
    schedule.every().day.at("19:30").do(search_user)
    schedule.every().hour.do(select_user_by_hour)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            time.sleep(1)
            print(e)
