from datetime import datetime

from dao.draw_dynamic_dao import DrawDynamicDao
from dao.follow_up_dao import FollowUpInfoDao
from dao.init_db import init_db
from dao.share_info_dao import ShareInfoDao
from dao.statistics_dao import StatisticsDao
from service.log_service.log_printer_service import MyLogger
from service.login_service.login_service import LoginService
from service.notify_service.notify_service import NotifyService
from service.remove_msg import RemoveMsgService
from service.share_service.share_one_dynamic import DynamicShareBase
from utils import globals
from utils.globals import get_random_comment_content, get_random_share_content
from utils.ip_util import remove_query_string
from utils.webdriver_util import init_webdriver

mylogger = MyLogger('share_from_biliLick.py').getLogger()


class BiliLinkShare(object):
    def __init__(self, user_id, bro=None, chains=None):
        db = init_db()
        self.share_note = ""
        self.user_id = user_id
        if bro is None:
            self.bro, self.chains = init_webdriver()
        else:
            self.bro = bro
            self.chains = chains
        self.share_info_dao = ShareInfoDao(db)
        self.follow_up_dao = FollowUpInfoDao(db)
        self.draw_dynamic_dao = DrawDynamicDao(db)
        self.statistics_dao = StatisticsDao(db)
        mylogger.error("启动：根据B站up主的分享链接进行抽奖动态转发!")

    def do_share_by_links(self):
        do_share_cnt = 0
        success_share_cnt = 0
        break_flag = 0
        try:
            LoginService(self.bro, self.chains, self.user_id).login_by_cookie()
            datas = self.get_today_dynamic_links()
            ignore_links = self.get_ignore_link()
            for data in datas:
                lucky_dynamic_url = remove_query_string(data['dyn_url'])
                # lucky_dynamic_url = 'https://www.bilibili.com/opus/886341319897645089'
                for ign_lnk in ignore_links:
                    if ign_lnk in lucky_dynamic_url:
                        break_flag = 1
                # 跳过已经转发过的
                if break_flag == 1:
                    break_flag = 0
                    continue
                break_flag = 0
                shared = self.share_info_dao.query_shareInfo_by_shareUrl(lucky_dynamic_url, self.user_id)
                if len(shared) != 0:
                    continue
                do_share_cnt = do_share_cnt + 1
                dyn = DynamicShareBase()
                dyn.user_id = self.user_id
                dyn.share_one(self.bro, self.chains, lucky_dynamic_url, get_random_share_content(), get_random_comment_content())
                # 保存转发状态和关注的up主信息
                if dyn.share_status == 0:
                    self.draw_dynamic_dao.update_sharedUrl(url=lucky_dynamic_url, status=1)
                    self.share_info_dao.insert_shareInfo(dyn)
                    self.follow_up_dao.saverUpdate(dyn.upId, dyn.upUrl, self.user_id)
                    success_share_cnt = success_share_cnt + 1
        except:
            mylogger.error("[do_share_by_links 根据url转发动态 出错]")
        finally:
            if do_share_cnt == 0:
                percentage = 0
            else:
                percentage = (success_share_cnt / do_share_cnt) * 100
            succ_percentage = f"成功率为 : {percentage:.2f}%"
            content = " 成功的转发条数为：" + str(success_share_cnt) + ";" + succ_percentage
            if 50 > percentage > 0:
                NotifyService().fangtang_msg_push_by_content(title="程序预警，需要处理！", content=content)
            self.statistics_dao.insert(self.user_id, content, "")
            # 暂时停止移除
            # RemoveMsgService(self.user_id, success_share_cnt, bro=self.bro, chains=self.chains).do_remove()
            self.bro.quit()

    def get_ignore_link(self):
        links = globals.ignore_link
        if len(links) != 0:
            return links.split('|')
        return {}

    def get_today_dynamic_links(self):
        """
        从数据库中获取当天的分享链接
        :return:
        """
        today = str(datetime.now().strftime("%Y-%m-%d"))
        return self.draw_dynamic_dao.query_by_time(today, limit=60, status=0)

