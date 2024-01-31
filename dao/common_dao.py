from dao.init_db import init_db


class CommonDao(object):
    def __init__(self, db):
        self.db = db

    def common_query(self, table_name="", cond_dict="", order="", fields="*"):
        try:
            """
            调用方法：
            data = common_query(table_name="t_share_info")
            data = common_query(table_name="t_share_info", order='order by id')
            data = common_query(table_name="t_share_info", cond_dict={'status': '0'}, order='order by id', fields=["id", "share_url"])
            """
            return self.db.select(table_name, cond_dict, order, fields)
        except Exception as e:
            return {}

    def common_insertMany(self, table, attrs, values):
        """
        调用方法：
        data = common_query(table_name="t_share_info")
        data = common_query(table_name="t_share_info", order='order by id')
        data = common_query(table_name="t_share_info", cond_dict={'status': '0'}, order='order by id', fields=["id", "share_url"])
        """
        try:
            self.db.insertMany(table, attrs, values)
            return 0
        except Exception as e:
            return 1

