import logging
import time
import traceback
from datetime import datetime
from time import sleep
from selenium.webdriver.common.by import By
import globals
from biz.login_by_cookie import login_by_cookie
from utils.customer_logger import error_to_log_more, error_to_log
from utils.mysql_operate import init_db
from utils.selenium_util import init_webdriver

logging.basicConfig(level=logging.INFO)


def is_draw(bro, xpath):
    """
    判断是否为抽奖标签
    :param bro:
    :param xpath:
    :return:
    """
    try:
        var = bro.find_element(By.XPATH, xpath).text
        if "抽奖" in var:
            return True
        else:
            return False
    except:
        return False


def do_share(bro, chains, fans_id, user_id):
    """
    真正执行转发的程序：
    1. 找到转发的动态，记录其dyn_id
    2. 根据dyn_id到动态详情页执行转发和评论操作
    3. 将转发的记录报错到t_share
    :param bro:
    :param chains:
    :param fans_id:
    :param user_id:
    :return:
    """
    try:
        url = 'https://space.bilibili.com/' + fans_id + '/dynamic'
        bro.get(url)
        sleep(2)
        i = 1
        share_list = bro.find_elements(By.XPATH, '//*[@id="page-dynamic"]/div[1]/div/div[1]/*/div/div')
        dyn_id_list = []
        """
        寻找满足抽奖条件的动态，将dyn_id记录下来，用于后面的执行转发操作
        """
        for x in share_list:
            try:
                # 获取动态转发的时间，我们这里只要看昨天或者今天的动态
                time = x.find_element(By.XPATH, './div[2]/div[2]').text
                if "小时" in time or "分钟" in time or "刚刚" in time or "昨天" in time:
                    # 判断是否互动抽奖
                    is_draw_name = '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' + str(
                        i) + ']/div/div/div[3]/div/div[2]'
                    if is_draw(bro, is_draw_name) is True:
                        dyn_id = x.find_element(By.XPATH,
                                                '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[' + str(i)
                                                + ']/div/div/div[3]/div/div[2]/div[3]/div').get_attribute("dyn-id")
                        dyn_id_list.append(dyn_id)
            except Exception as e1:
                logging.info("Retrying : find share list")
            i = i + 1
        logging.info("完成对 用户 : " + fans_id + " 是否有转发抽奖动态的判断， 该用户抽奖动态ID列表 : " + str(dyn_id_list))
        """
        执行转发操作：将前面记录的所以dyn_id进行访问，然后执行转发
        """
        db = init_db()
        for dyn_id in dyn_id_list:
            try:
                # 如果是已经转发过的，跳过，不转发
                sql = "SELECT * FROM t_share where dyn_id  = " + dyn_id
                data = db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
                if len(data) != 0:
                    break
                # 否则，开始执行下面的转发操作
                new_url = 'https://t.bilibili.com/' + dyn_id
                bro.get(new_url)
                sleep(3)

                # 移动到头像
                touxiang = bro.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div')
                sleep(3)
                chains.move_to_element(touxiang).perform()
                sleep(3)

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
                                                '//*[@id="app"]/div[2]/div/div/div[2]/div[1]/div[1]/div/div[2]/div['
                                                '2]/div[2]/button')
                sleep(2)
                chains.click(do_share_btn).perform()
                sleep(2)

                # 保存记录
                params = {
                    'user_id': user_id,
                    'fans_id': fans_id,
                    'dyn_id': dyn_id,
                    'flag': str(1),
                    'insert_time': str(datetime.now())
                }
                db.insert('t_share', params)
                # 更新t_share的update_time
                update_params = {'update_time': str(datetime.now())}
                cond_dict = {'fans_id': fans_id}
                db.update('t_fans', update_params, cond_dict)
            except Exception as e:
                error_to_log_more("start_forward", "转发动态[执行转发or入库]出错：" + traceback.format_exc(), "p1", dyn_id)
    except Exception as e:
        logging.error(traceback.format_exc())


def get_fans_list():
    """
    获取2023年中还有进行经常转发动态的用户
    这里设置2023年之后是为了防止以前筛选的用户是僵尸用户
    :return:
    """
    try:
        db = init_db()
        sql = "SELECT * FROM t_fans where update_time >= '2023';"
        data = db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
        list = []
        for fans in data:
            list.append(fans['fans_id'])
        return list
    except Exception as e1:
        error_to_log("get_fans_list", "获取用户列表出错：" + traceback.format_exc(), "p0")
        logging.error(traceback.format_exc())


def start_forward():
    """
    从t_fans表中获取用户ids_list
    对ids_list中的用户，扫描其中是否在昨天有转发动态，如果有，则执行转发操作，同时将转发记录保存到t_share表中
    :return:
    """
    try:
        logging.info('抽奖动态开始转发，当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        # 初始化
        bro, chains = init_webdriver()
        cookie_path = './cookie/' + globals.my_user_id + '.txt'
        bro.get(globals.home_url)
        login_by_cookie(bro, cookie_path)
        # 从t_fans表获取用户ID列表
        ids_list = get_fans_list()
        # 执行转发操作
        i = 1
        for id in ids_list:
            do_share(bro, chains, id, globals.my_user_id)
            logging.info("No:  " + str(i) + ", userId = " + id + ' finish share!')
            i = i + 1
    except Exception as e:
        error_to_log("start_forward", "转发动态出错：" + traceback.format_exc(), "p1")
    finally:
        finish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        logging.info('抽奖动态转发结束，当前时间：' + finish_time)

