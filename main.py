import logging
import traceback

import schedule
import time
from biz.draw_dynamic_share import start_forward
from biz.get_user import select_user_by_hour, search_user
from utils.customer_logger import error_to_log

logging.basicConfig(level=logging.INFO)




if __name__ == '__main__':



    logging.info("start main task")
    select_user_by_hour();
    # select_user_by_hour()

    # start_forward()
    # search_user()
    schedule.every().day.at("00:36").do(search_user)
    schedule.every().day.at("00:36").do(start_forward)
    schedule.every().hour.do(select_user_by_hour)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            time.sleep(1)
            print(e)
