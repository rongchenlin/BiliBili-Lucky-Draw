import logging
import traceback
import schedule
import time
from biz.draw_dynamic_share import start_forward
from biz.get_user import select_user_by_hour, search_user
from biz.login_by_cookie import check_cookie_valid
from utils.customer_logger import error_to_log

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    login_valid = check_cookie_valid()
    if login_valid is False:
        logging.error("超时未登录，程序退出！")
    logging.info("start dynamic share task")
    time.sleep(10)
    start_forward()
    schedule.every().day.at("15:42").do(search_user)
    schedule.every().day.at("15:45").do(start_forward)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            time.sleep(1)
            logging.error("每小时筛选用户任务出错：" + traceback.format_exc())
