from dao.init_db import init_db
from service.share_service.share_one_dynamic import DynamicShareBase


class ShareInfoDao(object):
    def __init__(self, db):
        self.table_name = 't_share_info'
        self.db = db

    def query_shareInfo_by_userIdAndTime(self,  user_id, share_time):
        """
        根据转发的url查询
        :param user_id:
        :param share_url:
        :return:
        """
        try:
            sql = "SELECT * FROM " + self.table_name + " where user_id = '" + user_id + "'" + " and share_time >= '" + share_time + "'";
            data = self.db.select_db(sql)
            return data
        except Exception as e:
            return {}

    def query_shareInfo_by_shareUrl(self, share_url, user_id):
        """
        根据转发的url查询
        :param user_id:
        :param share_url:
        :return:
        """
        try:
            sql = "SELECT * FROM " + self.table_name + " where share_url = '" + share_url + "'" + " and user_id = '" + user_id + "'";
            data = self.db.select_db(sql)
            return data
        except Exception as e:
            return {}


    def insert_shareInfo(self, shareInfo):
        try:
            params = {}
            params['upId'] = str(shareInfo.upId)
            params['upUrl'] = str(shareInfo.upUrl)
            params['share_url'] = str(shareInfo.share_url)
            params['status'] = str(shareInfo.status)
            params['machine_ip'] = str(shareInfo.machine_ip)
            params['share_time'] = str(shareInfo.share_time)
            params['user_id'] = str(shareInfo.user_id)
            params['share_status'] = str(shareInfo.share_status)
            self.db.insert(self.table_name, params)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    db = init_db()
    shareInfodao = ShareInfoDao(db)
    # dyn = DynamicShareBase()
    # dyn.upUrl = '1'
    # dyn.upId = '2'
    # dyn.share_url = '2share_url'
    # dyn.status = 1
    # dyn.machine_ip = '2machine_ip'
    # dyn.share_time = '2022-12-12'
    # dyn.share_status = 1


