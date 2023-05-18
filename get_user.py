import datetime
import time
from datetime import datetime
from time import sleep

from selenium.webdriver.common.by import By

from utils.customer_logger import error_to_log
from utils.mysql_operate import init_db
from utils.selenium_util import is_xpath_exist, init_webdriver2
from utils.time_util import deal_time


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

def select_user_by_hour():
    try:
        # 初始化打开数据库连接
        print('开始筛选，当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        db = init_db('bilibili')
        sql = "SELECT * FROM t_users_cnt order by insert_time desc "  # sql语句，可自行对应自己数据相应的表进行操作
        data = db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
        max_id = int(data[0]['user_id'])
        # 初始化
        bro, chains = init_webdriver2()
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
def search_user():
    try:
        print('开始搜索用户，当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
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

# if __name__ == '__main__':
#     print("start search users task")
#     select_user_by_hour()
#     schedule.every().day.at("07:30").do(search_user)
#     schedule.every().day.at("19:30").do(search_user)
#     schedule.every().hour.do(select_user_by_hour)
#     while True:
#         try:
#             schedule.run_pending()
#             time.sleep(1)
#         except Exception as e:
#             time.sleep(1)
#             print(e)
