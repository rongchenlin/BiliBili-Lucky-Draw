import logging
import socket
import traceback
from datetime import datetime
from utils.mysql_operate import init_db

logging.basicConfig(level=logging.INFO)


def error_to_log(function_name, content, note):
    try:
        logging.error("出错的方法名：" + function_name + " 出错内容: " + content + " 错误级别：" + note)
        ip = get_host_ip()
        db = init_db()
        # 保存记录
        params = {}
        params['function_name'] = function_name
        params['content'] = str(content).replace('"', '').replace("'", '')[:2500]
        params['note'] = note
        params['ip'] = ip
        params['insert_time'] = str(datetime.now())
        db.insert('t_log', params)
    except Exception as e:
        logging.error(traceback.format_exc())


def print_run_time(name, begin_time, end_time):
    """
    计算运行时间
    :param name:
    :param begin_time:
    :param end_time:
    :return:
    """
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
        db = init_db()
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
        logging.error(traceback.format_exc())


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



