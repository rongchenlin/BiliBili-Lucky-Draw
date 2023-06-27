import datetime
import logging
import time
import traceback
from time import sleep
from selenium.webdriver.common.by import By
import globals
from biz.login_by_cookie import login_by_cookie
from utils.customer_logger import error_to_log
from utils.mysql_operate import init_db
from utils.selenium_util import init_webdriver
from utils.time_util import deal_time
from utils.xpath_util import is_xpath_exist

logging.basicConfig(level=logging.INFO)

def search_user():
    try:
        db = init_db()
        dayAgo = (datetime.datetime.now() - datetime.timedelta(days=100))
        # 转换为其他字符串格式
        dayAgo = dayAgo.strftime("%Y-%m-%d")
        sql = "SELECT * FROM `t_users_cnt` where TO_DAYS( NOW()) - TO_DAYS(insert_time) =1;"
        list = db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
        for data in list:
            try:
                d_time = data['last_draw_time']
                d_time = deal_time(d_time)
                if d_time >= dayAgo:
                    sql2 = "SELECT * FROM t_fans where fans_id  = " + data['user_id']
                    data2 = db.select_db(sql2)
                    if len(data2) != 0:
                        continue
                    # 保存记录
                    params = {
                        'fans_id': data['user_id'],
                        'flag': str(data['draw_cnt']),
                        'insert_time': str(datetime.datetime.now()),
                        'update_time': d_time
                    }
                    db.insert('t_fans', params)
            except Exception as e:
                continue
    except Exception as e:
        error_to_log("search_user", "二级筛选用户出错：" + traceback.format_exc(), "无")



def check_user(bro, chains, fans_id):
    """
    判断fans_id这个用户是否为经常转发动态的用户，如果是将数据保存到t_user_cnt
    :param bro:
    :param chains:
    :param fans_id:
    :return:
    """
    try:
        db = init_db()
        url = 'https://space.bilibili.com/' + fans_id + '/dynamic'
        bro.get(url)
        sleep(2)
        share_list = bro.find_elements(By.XPATH, '//*[@id="page-dynamic"]/div[1]/div/div[1]/*/div/div')
        i = 1
        draw_cnt = 0
        for x in share_list:
            try:
                time = x.find_element(By.XPATH, './div[2]/div[2]').text
                # 判断是否互动抽奖
                is_draw_name = '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' + str(
                    i) + ']/div/div/div[3]/div/div[2]/div[2]/div/div[1]/span[2]'
                if is_xpath_exist(bro, is_draw_name) is True:
                    draw_cnt = draw_cnt + 1
                    last_draw_time = time
            except Exception as e:
                error_to_log("check_user", "每小时扫描用户程序[判断是否互动抽奖]出错：" + traceback.format_exc(), "p3")
                continue
            i = i + 1
        if draw_cnt >= globals.check_ok_draw_time:
            try:
                # 保存记录
                params = {}
                params['user_id'] = fans_id
                params['draw_cnt'] = str(draw_cnt)
                params['last_time'] = time
                params['last_draw_time'] = last_draw_time
                params['insert_time'] = str(datetime.datetime.now())
                db.insert('t_users_cnt', params)
            except Exception as e:
                error_to_log("check_user", "每小时扫描用户程序[保存数据库到t_user_cnt]出错：" + traceback.format_exc(), "p3")
        sleep(2)
    except Exception as e:
        error_to_log("check_user", "每小时扫描用户程序出错：" + traceback.format_exc(), "p3")


def get_max_userid():
    """
    获取用户初筛表中目前的最大ID作为本次开始扫描的ID
    :return: 最大ID
    """
    db = init_db()
    sql = "SELECT * FROM t_users_cnt where draw_cnt != -100 order by insert_time desc "
    data = db.select_db(sql)
    max_id = int(data[0]['user_id'])
    return max_id


def select_user_by_hour():
    """
    每小时定时任务初筛经常转发动态的用户，并将结果报错到t_user_cnt表中
    :return:
    """
    bro = None
    start_id = 0
    try:
        logging.info('开始筛选经常转发抽奖动态的B站用户，当前时间：' +
                     time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        # TODO 为了避免验证码问题，这里先登录，后续用其他方式解决
        bro, chains = init_webdriver()
        cookie_path = './cookie/' + globals.my_user_id + '.txt'
        bro.get(globals.home_url)
        login_by_cookie(bro, cookie_path)
        # 每次扫描开始的ID
        start_id = get_max_userid()
        # 开始扫描，每次只设置400个
        for i in range(1, 400):
            id = str(start_id + i)
            check_user(bro, chains, id)
            logging.info("No: " + str(i) + ", userId = " + id + ' 被扫描，初筛完成!')
    except Exception as e:
        error_to_log("select_user_by_hour", "每小时扫描用户程序出错：" + traceback.format_exc(), "p3")
    finally:
        try:
            # 设置一个不用的ID作为下次开始的标志位
            flag_id = str(start_id + 401)
            db = init_db()
            params = {}
            params['user_id'] = flag_id
            params['draw_cnt'] = str(-100)
            params['last_time'] = str(datetime.datetime.now())
            params['last_draw_time'] = str(datetime.datetime.now())
            params['insert_time'] = str(datetime.datetime.now())
            db.insert('t_users_cnt', params)
        except Exception as e:
            error_to_log("check_user", "每小时扫描用户程序[消息入口]出错：" + traceback.format_exc(), "p3")
        if bro is not None:
            bro.quit()
        logging.info('出筛结束，当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

