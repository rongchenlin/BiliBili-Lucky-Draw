import logging
import os
import time
import traceback
import schedule
from biz.get_user import select_user_by_hour
from biz.login_by_cookie import check_cookie_valid
from globals import max_checks, my_user_id

logging.basicConfig(level=logging.INFO)




if __name__ == '__main__':

    login_valid = check_cookie_valid()
    if login_valid is False:
        logging.error("超时未登录，程序退出！")

    logging.info("start hourly search user task")
    time.sleep(10)
    select_user_by_hour()
    schedule.every().hour.do(select_user_by_hour)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            time.sleep(1)
            logging.error("每小时筛选用户任务出错：" + traceback.format_exc())
