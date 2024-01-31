import socket

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


def get_partContent_from_lick(current_url):
    user_id = '0'
    parts = current_url.split('/')
    if len(parts) > 1:
        user_id = parts[3]
    return user_id

def remove_query_string(url):
    question_mark_index = url.find('?')

    if question_mark_index != -1:
        # 如果包含问号，则去掉问号及其后面的内容
        url_without_query = url[:question_mark_index]
        return url_without_query
    else:
        # 如果不包含问号，则返回原始url
        return url