import logging

import pymysql

from utils.mysql_operate import MysqldbHelper

from utils.globals import db_host, port, user, passwd, charset, dbname


def init_db():
    """
    初始化数据库连接
    :return:
    """
    config = {
        'host': db_host,
        'port': port,
        'user': user,
        'passwd': passwd,
        'charset': charset,
        'cursorclass': pymysql.cursors.DictCursor
    }
    logging.warning("ip :" + str(db_host))
    logging.info("db info :")
    logging.info(config)
    db = MysqldbHelper(config)
    db.selectDataBase(dbname)
    logging.warning("创建数据库连接信息 :" + str(config))
    return db

