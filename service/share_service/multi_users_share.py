from service.log_service.log_printer_service import MyLogger
from service.search_draw_dynamic_service.SearchDynamicByUps import SearchDynamicByUps
from service.share_service.share_from_biliLink import BiliLinkShare
from utils import globals

mylogger = MyLogger('multi_users_share.py').getLogger()


class MultiUsersShareService(object):
    """
    多用户转发模式
    """

    def __init__(self):
        mylogger.error('启动多用户转发模式!')


    def do_multi_uses_share(self):
        try:
            users = self.get_multi_uses()
            for user in users:
                mylogger.error('用户: ' + user + '开始转发动态.')
                BiliLinkShare(user).do_share_by_links()
        except Exception as e:
            mylogger.error("[do_multi_uses_share 多用户模式转发动态 出错 %s]" % e, exc_info=True)

    def get_multi_uses(self):
        users = globals.multi_users
        if len(users) != 0:
            return users.split('|')
        return {}
