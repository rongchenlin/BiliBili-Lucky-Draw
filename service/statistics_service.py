from datetime import datetime
from dao.draw_dynamic_dao import DrawDynamicDao
from dao.init_db import init_db
from dao.share_info_dao import ShareInfoDao
from utils import globals


class StatisticsService(object):

    def __init__(self):
        db = init_db()
        self.share_info_dao = ShareInfoDao(db)
        self.dyn_dao = DrawDynamicDao(db)

    def get_today_searchData(self):
        try:
            # 获取今天的日期
            today = datetime.now()
            today_str = today.strftime("%Y-%m-%d")
            return self.dyn_dao.query_by_time(today_str, status=1)
        except Exception as e:
            return {}

    def get_today_shareData_by_usrId(self, user_id):
        try:
            # 获取今天的日期
            today = datetime.now()
            today_str = today.strftime("%Y-%m-%d")
            return self.share_info_dao.query_shareInfo_by_userIdAndTime(user_id, today_str)
        except Exception as e:
            return {}

    def today_data(self):
        userIds = self.get_multi_uses()
        content = "今日数据汇总: " + "\n\n"

        content = content + "1.抽奖动态搜索数量: " + str(len(self.get_today_searchData())) + ";\n\n"
        content = content + "2.动态转发情况: " + "\n\n"
        for user_id in userIds:
            content = content + "\t\t" + user_id + ":" + "成功转发数量:" + str(len(self.get_today_shareData_by_usrId(user_id))) + ";\n\n"
        content = content + "\n\n"
        cnt = len(userIds)
        return cnt, content

    def get_multi_uses(self):
        users = globals.multi_users
        if len(users) != 0:
            return users.split('|')
        return {}
