import logging
import os
from utils.file_util import get_value_from_env

logging.basicConfig(level=logging.INFO)


def check_cookie_status():
    try:
        file_name = ''
        if os.path.exists(os.path.join('./', '.env')):
            # 加载 .env 文件
            my_user_id_value = get_value_from_env(".env", "my_user_id")
            file_name = my_user_id_value + '.txt'
        if os.path.exists(os.path.join('./cookie', file_name)):
            return True
        else:
            return False
    except Exception as e:
        return False
