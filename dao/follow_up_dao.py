from datetime import datetime

class FollowUpInfoDao(object):
    def __init__(self,db):
        self.db = None
        self.table_name = 't_followdups'
        self.db = db
    def query_followUpInfo_by_UpId(self, up_id, user_id):
        try:
            sql = "SELECT * FROM " + self.table_name + " where up_id = '" + up_id + "'" + " and user_id = '" + user_id + "'";
            data = self.db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
            return data
        except Exception as e:
            return {}


    def saverUpdate(self, up_id, up_url, user_id):
        try:
            params = {}
            params['up_id'] = str(up_id)
            params['user_id'] = str(user_id)
            params['up_url'] = str(up_url)
            params['update_time'] = str(datetime.now())
            data = self.query_followUpInfo_by_UpId(up_id, user_id)
            if len(data) == 0:
                params['status'] = str(1)
                self.db.insert(self.table_name, params)
            else:
                status = int(data[0]['status'])
                status = status + 1
                params['status'] = str(status)
                cond_dict = {'up_id': up_id,'user_id': user_id}
                self.db.update(self.table_name, params, cond_dict)
        except Exception as e:
            print(e)


