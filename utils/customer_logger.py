import logging
import socket
from datetime import datetime

from utils.mysql_operate import init_db

logging.basicConfig(level=logging.INFO)

def error_to_log(function_name, content, note):
    try:
        ip = get_host_ip()
        db = init_db('bilibili')
        # 保存记录
        params = {}
        params['function_name'] = function_name
        params['content'] = str(content).replace('"', '').replace("'", '')[:2500]
        params['note'] = note
        params['ip'] = ip
        params['insert_time'] = str(datetime.now())
        db.insert('t_log', params)
    except Exception as e:
        logging.error(e)
    # finally:
    #     # db.close()
    #     print("日志完成入库")


def print_run_time(name, begin_time, end_time):
    run_time = round(end_time - begin_time)
    # 计算时分秒
    hour = run_time // 3600
    minute = (run_time - 3600 * hour) // 60
    second = run_time - 3600 * hour - 60 * minute
    run_time_show = f'\r\n\r\n{name} 总共运行时间：{hour}小时{minute}分钟{second}秒'
    return run_time_show

def error_to_log_more(function_name, content, note, retry_dyn_id):
    try:
        ip = get_host_ip()
        db = init_db('bilibili')
        # 保存记录
        params = {}
        params['function_name'] = function_name
        params['content'] = str(content).replace('"', '').replace("'", '')[:2500]
        params['note'] = note
        params['ip'] = ip
        params['retry_dyn_id'] = retry_dyn_id
        params['insert_time'] = str(datetime.now())
        db.insert('t_log', params)
    except Exception as e:
        logging.error(e)

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip



