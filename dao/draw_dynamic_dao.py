from datetime import datetime


class DrawDynamicDao(object):
    def __init__(self, db):
        self.table_name = 't_draw_dynamic'
        self.db = db

    def query_by_time(self, time, limit=2000, status=1):
        try:
            sql = ("SELECT * FROM " + self.table_name
                   + " where status = '" + str(status)
                   + "' and insert_time >= '" + time
                   + "' limit " + str(limit))
            data = self.db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
            return data
        except Exception as e:
            return {}

    def query_by_dyn_url(self, dyn_url):
        try:
            sql = "SELECT * FROM " + self.table_name + " where dyn_url = '" + dyn_url + "'";
            data = self.db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
            return data
        except Exception as e:
            return {}

    def insert(self, dyn_url, source, note):
        try:
            params = {}
            params['dyn_url'] = str(dyn_url)
            params['source'] = str(source)
            params['status'] = '0'
            params['note'] = str(note)
            params['insert_time'] = str(datetime.now())
            self.db.insert(self.table_name, params)
            return True
        except Exception as e:
            return False

    def update_sharedUrl(self, url, status):
        try:
            params = {'status': str(status)}
            cond_dict = {'dyn_url': url}
            self.db.update(self.table_name, params, cond_dict)
        except Exception as e:
            print(e)
