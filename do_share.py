import json
import logging
import socket
import threading
# 实现无可视化界面
# 实现规避检测
import time
from datetime import datetime
from time import sleep

import requests
import schedule
from selenium.webdriver.common.by import By

from get_user import select_user_by_hour, search_user
from utils.mysql_operate import init_db
from utils.selenium_util import init_webdriver

logging.basicConfig(level=logging.INFO)

def error_to_log_more(function_name, content, note, retry_dyn_id):
    try:
        ip = get_host_ip()
        db = init_db('bilibili')
        # 保存记录
        params = {}
        params['function_name'] = function_name
        params['content'] = str(content).replace('"', '').replace("'", '')[:2500]
        params['note'] = note
        params['ip'] = ip
        params['retry_dyn_id'] = retry_dyn_id
        params['insert_time'] = str(datetime.now())
        db.insert('t_log', params)
    except Exception as e:
        logging.error(e)


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
        logging.error(e)
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
        logging.info('login by cookie success !')
        sleep(1)
    except Exception as e:
        logging.error('login by cookie fail !')
        error_to_log("login_by_cookie", "cookie登录失败", "p0")


def is_xpath_exist(bro, xpath):
    try:
        bro.find_element(By.XPATH, xpath)
        return True
    except:
        return False


def is_draw(bro, xpath):
    try:
        var = bro.find_element(By.XPATH, xpath).text
        if "抽奖" in var:
            return True
        else:
            return False
    except:
        return False


def do_share(bro, chains, fans_id, userId):
    try:
        url = 'https://space.bilibili.com/' + fans_id + '/dynamic'
        bro.get(url)
        sleep(5)
        i = 1
        share_list = bro.find_elements(By.XPATH, '//*[@id="page-dynamic"]/div[1]/div/div[1]/*/div/div')
        dyn_id_list = []
        flag = False
        for x in share_list:
            attempt = 0
            success = False
            while attempt < 5 and not success:
                try:
                    time = x.find_element(By.XPATH, './div[2]/div[2]').text
                    # if "小时" in time or "分钟" in time or "刚刚" in time or "昨天" in time or "02-0" in time:
                    if "小时" in time or "分钟" in time or "刚刚" in time or "昨天" in time:
                        # 判断是否互动抽奖
                        is_draw_name = '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' + str(
                            i) + ']/div/div/div[3]/div/div[2]'
                        if is_draw(bro, is_draw_name) is True:
                            # success = True
                            dyn_id = x.find_element(By.XPATH,
                                                    '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' + str(
                                                        i) + ']/div/div/div[3]/div/div[2]/div[3]/div').get_attribute(
                                "dyn-id")
                            # 保存所有的要转发的ID
                            dyn_id_list.append(dyn_id)
                    success = True
                except Exception as e1:
                    attempt = attempt + 1
                    logging.info("Retrying : find share list")
                    sleep(1 + attempt * 5)
                    if attempt == 5:
                        flag = True
                        logging.warning('Retry Up 5 Times, try to refresh url')
                        break
            i = i + 1

        if flag is True:
            logging.warning('refresh url .....')
            url = 'https://space.bilibili.com/' + fans_id + '/dynamic'
            bro.get(url)
            sleep(5)
            i = 1
            share_list = bro.find_elements(By.XPATH, '//*[@id="page-dynamic"]/div[1]/div/div[1]/*/div/div')
            for x in share_list:
                attempt = 0
                success = False
                while attempt < 5 and not success:
                    try:
                        time = x.find_element(By.XPATH, './div[2]/div[2]').text
                        if "小时" in time or "分钟" in time or "刚刚" in time or "昨天" in time:
                            # 判断是否互动抽奖
                            is_draw_name = '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' + str(
                                i) + ']/div/div/div[3]/div/div[2]'
                            if is_draw(bro, is_draw_name) is True:
                                # success = True
                                dyn_id = x.find_element(By.XPATH,
                                                        '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' + str(
                                                            i) + ']/div/div/div[3]/div/div[2]/div[3]/div').get_attribute(
                                    "dyn-id")
                                # 保存所有的要转发的ID
                                dyn_id_list.append(dyn_id)
                        success = True
                    except Exception as e1:
                        attempt = attempt + 1
                        logging.info("Retrying : find share list")
                        sleep(1 + attempt * 5)
                        if attempt == 5:
                            logging.error("Retrying Fail, Error To DB: find share list fail!")
                            error_to_log("start_forward",
                                         "fans_id: " + fans_id + " 转发动态[寻找转发列表]出错：" + repr(e1), "p2")
                            break
                i = i + 1

        db = init_db('bilibili')
        logging.info("current user dyn_id_list: " + str(dyn_id_list))
        # logging.info(dyn_id_list)
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
                    sleep(5)

                    # 移动到头像
                    touxiang = bro.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div')
                    sleep(2)
                    chains.move_to_element(touxiang).perform()
                    sleep(2)

                    # 点击关注
                    follow = bro.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[3]/div[1]')
                    follow_text = follow.get_attribute('innerText')
                    sleep(2)
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
                    sleep(2)
                    chains.click(do_share_btn).perform()
                    sleep(2)

                    # 保存记录
                    params = {}
                    params['user_id'] = userId
                    params['fans_id'] = fans_id
                    params['dyn_id'] = dyn_id
                    params['flag'] = str(1)
                    params['insert_time'] = str(datetime.now())
                    db.insert('t_share', params)

                    # 更新t_share的update_time
                    params = {}
                    params['update_time'] = str(datetime.now())
                    cond_dict = {}
                    cond_dict['fans_id'] = fans_id
                    db.update('t_fans', params, cond_dict)

                    success = True
                except Exception as e2:
                    attempt = attempt + 1
                    sleep(5)
                    if attempt == 3:
                        error_to_log_more("start_forward", "转发动态[执行转发or入库]出错：" + json.dumps(e2), "p1",
                                          dyn_id)
                        break
    except Exception as e3:
        logging.error(e3)


def get_fans_list():
    try:
        db = init_db('bilibili')
        sql = "SELECT * FROM t_fans where update_time >= '2023';"
        data = db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
        list = []
        for fans in data:
            list.append(fans['fans_id'])
        return list
    except Exception as e1:
        error_to_log("get_fans_list", "获取用户列表出错：" + repr(type(e1)), "p0")
        logging.error(e1)


def start_forward():
    try:
        begin_time = time.time()
        print('开始转发，当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        logging.info(start_time)
        # 初始化打开数据库连接
        db = init_db('bilibili')
        userId = '433441242'
        # userId = '385649497'
        cookie_path = './cookie/' + userId + '.txt'
        homeUrl = 'https://www.bilibili.com/'
        # 初始化
        bro, chains = init_webdriver()
        bro.get(homeUrl)

        # 登录
        # login_manual(bro, cookie_path)
        login_by_cookie(bro, cookie_path)

        # 获取用户ID列表
        ids_list = get_fans_list()
        list_len = len(ids_list)
        # 执行转发操作
        i = 1
        for id in ids_list:
            do_share(bro, chains, id, userId)
            logging.info("No:  " + str(i) + ", userId = " + id + ' finish share!')
            i = i + 1
    except Exception as e2:
        error_to_log("start_forward", "转发动态出错：" + repr(type(e2)), "p1")
    finally:
        end_time = time.time()
        finish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        logging.info(finish_time)
        run_time_show = print_run_time("动态转发程序", begin_time, end_time)

        try:
            logging.info('开始转发')
            url1 = 'https://sctapi.ftqq.com/SCT172323TZn2oLYosf0TJY80XSH7KN29R.send'
            url2 = 'https://sctapi.ftqq.com/SCT63874Tus7GmUoMlz6b2iJNxrQ1gUws.send'
            desp = '动态转发程序\r\n\r\n开始运行时间：' + start_time + '\r\n\r\n结束运行时间：' + finish_time + run_time_show + '\r\n\r\n扫描的用户数量：' + str(
                list_len)
            data = {
                'title': '动态转发数据统计',
                'desp': desp,
                'short': '动态转发数据统计'
            }
            r = requests.post(url1, data)
            r = requests.post(url2, data)
        except Exception as e2:
            error_to_log("send_start_forward", "筛选任务开始发送通知出错：" + repr(type(e2)), "无")

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


def print_run_time(name, begin_time, end_time):
    run_time = round(end_time - begin_time)
    # 计算时分秒
    hour = run_time // 3600
    minute = (run_time - 3600 * hour) // 60
    second = run_time - 3600 * hour - 60 * minute
    run_time_show = f'\r\n\r\n{name} 总共运行时间：{hour}小时{minute}分钟{second}秒'
    return run_time_show


if __name__ == '__main__':

    logging.info("start main task")
    schedule.every().day.at("11:10").do(search_user)
    schedule.every().day.at("11:13").do(start_forward)
    schedule.every().hour.do(select_user_by_hour)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            time.sleep(1)
            print(e)
