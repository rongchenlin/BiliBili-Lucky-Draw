import time
import schedule
from service.search_draw_dynamic_service.SearchDynamicByUps import SearchDynamicByUps
from service.share_service.multi_users_share import MultiUsersShareService
from utils import globals


def do_search():
    SearchDynamicByUps(globals.my_user_id).init_search()
def do_share():
    MultiUsersShareService().do_multi_uses_share()

if __name__ == '__main__':
    time.sleep(15)
    do_search()
    do_share()

    schedule.every().day.at("15:42").do(do_search)
    schedule.every().day.at("15:45").do(do_share)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            time.sleep(1)



