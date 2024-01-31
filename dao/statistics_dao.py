from datetime import datetime, timedelta

from dao.init_db import init_db


class StatisticsDao(object):
    def __init__(self, db):
        self.table_name = 't_statistics'
        self.db = db

    def query_by_time(self, time):
        try:
            sql = "SELECT * FROM " + self.table_name + " where insert_time >= '" + time + "'";
            data = self.db.select_db(sql)  # 用mysql_operate文件中的db的select_db方法进行查询
            return data
        except Exception as e:
            return {}



    def query_today_data(self):
        # 获取今天的日期
        today = datetime.now()
        # 计算昨天的日期
        yesterday = today - timedelta(days=1)
        # 将日期格式化为字符串
        yesterday_str = yesterday.strftime("%Y-%m-%d")

        today_str = today.strftime("%Y-%m-%d")
        text = ""
        datas = self.query_by_time(today_str)
        for data in datas:
            text = text + str(data['insert_time']) + "\n内容:[" + data['user_id'] + data['content'] + "]\n备注:[" + data['note'] + "]\n\n"
        return text

    def insert(self, user_id, content, note):
        try:
            params = {'user_id': str(user_id), 'content': str(content), 'note': str(note),
                      'insert_time': str(datetime.now())}
            self.db.insert(self.table_name, params)
            return True
        except:
            return False
