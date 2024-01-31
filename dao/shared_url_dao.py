from datetime import datetime

from dao.init_db import init_db
from service.share_service.share_one_dynamic import DynamicShareBase


class SharedUrlDao(object):
    def __init__(self, db):
        self.table_name = 't_shared_urls'
        self.db = db

    def query_sharedUrls_limit(self, user_id, status, limit):
        """
        根据转发的url查询
        :param user_id:
        :param share_url:
        :return:
        """
        try:
            sql = ("SELECT * FROM " + self.table_name
                   + " where user_id = '" + user_id + "'" + " and status = '" + status + "'"
                   + " ORDER BY dyn_url"
                   + " limit " + str(limit) + ";");
            data = self.db.select_db(sql)
            return data
        except Exception as e:
            print(e)
            return {}

    def insert_sharedUrl(self, user_id, url):
        try:
            params = {'dyn_url': str(url), 'user_id': user_id, 'insert_time': str(datetime.now()), 'status': '0'}
            self.db.insert(self.table_name, params)
        except Exception as e:
            print(e)

    def update_sharedUrl(self, user_id, url, status):
        try:
            params = {'update_time': str(datetime.now()), 'status': str(status)}
            cond_dict = {'dyn_url': url, 'user_id': user_id}
            self.db.update(self.table_name, params, cond_dict)
        except Exception as e:
            print(e)
