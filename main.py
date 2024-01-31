from dao.init_db import init_db
from dao.shared_url_dao import SharedUrlDao
from service.login_service.login_service import LoginService
from service.remove_msg import RemoveMsgService
from service.remove_share import RemoveShareService
from service.search_draw_dynamic_service.SearchDynamicByUps import SearchDynamicByUps
from service.share_service.multi_users_share import MultiUsersShareService
from service.share_service.share_from_biliLink import BiliLinkShare
from utils import globals
from utils.webdriver_util import init_webdriver

if __name__ == '__main__':
    # 多用户转发
    if globals.do_type == 'multi':
        # SearchDynamicByUps(globals.my_user_id).init_search()
        MultiUsersShareService().do_multi_uses_share()
    # 手动登录
    if globals.do_type == 'login_manual':
        bro, chians = init_webdriver()
        LoginService(bro, chians).login_manual()
    # 手动登录
    if globals.do_type == 'auto_login':
        bro, chians = init_webdriver()
        LoginService(bro, chians, globals.my_user_id).login_by_cookie()
        input()
    # 单用户
    if globals.do_type == 'single':
        SearchDynamicByUps(globals.my_user_id).init_search()
        BiliLinkShare(globals.my_user_id).do_share_by_links()