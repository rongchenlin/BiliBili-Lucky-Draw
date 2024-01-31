import requests

from dao.init_db import init_db
from dao.statistics_dao import StatisticsDao
from utils import globals

class NotifyService(object):

    def __init__(self):
        self.key = globals.FangTang_KEY
        self.statistics_dao = StatisticsDao(init_db())


    def fangtang_msg_push(self):
        """
        方糖
        https://zhuanlan.zhihu.com/p/377659574
        https://sct.ftqq.com/sendkey
        :return:
        """
        try:
            self.text = self.statistics_dao.query_today_data()
            url = 'https://sc.ftqq.com/%s.send' % self.key
            requests.post(url, data={'text': "程序通知", 'desp': self.text})
        except Exception as e:
            print()

    def fangtang_msg_push_by_content(self, title="", content=""):
        """
        方糖
        https://zhuanlan.zhihu.com/p/377659574
        https://sct.ftqq.com/sendkey
        :param key:
        :return:
        """
        try:
            url = 'https://sc.ftqq.com/%s.send' % self.key
            if globals.notify_switch == 'Y':
                requests.post(url, data={'text': title, 'desp': content})
        except Exception as e:
            print()


if __name__ == '__main__':
    # NotifyService().fangtang_msg_push(key="b0e892e8856d5a45a415c739489b13b9")
    print()
