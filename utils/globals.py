import os
import random

from dotenv import load_dotenv

from utils.ip_util import get_host_ip

# 加载 .env 文件
load_dotenv()
# 读取变量
max_checks = int(os.getenv("max_checks"))
home_url = os.getenv("home_url")
my_user_id = os.getenv("my_user_id")
ignore_link = os.getenv("ignore_link")
multi_users = os.getenv("multi_users")
do_type = os.getenv("do_type")
is_remove = os.getenv("is_remove")
remove_cnt = os.getenv("remove_cnt")
cookie_value = os.getenv("cookie_value")
# 读取变量
dbname = os.getenv("MYSQL_DATABASE")
user = os.getenv("MYSQL_USER")
passwd = os.getenv("MYSQL_PASSWORD")
root_passwd = os.getenv("MYSQL_ROOT_PASSWORD")
port = int(os.getenv("PORT"))
charset = 'utf8'

notify_switch = os.getenv("notify_switch")
FangTang_KEY = os.getenv("FangTang_KEY")
DRIVER_VERSION = os.getenv("DRIVER_VERSION")


def getHost():
    host = get_infos("DB_HOST")
    print(host)
    if len(host) != 0:
        return host
    return get_host_ip()


def get_infos(str):
    users = os.getenv(str)
    return users


def get_random_comment_content():
    comments = get_multi_infos("comment_content")
    return get_random_from_list(comments)


def get_random_share_content():
    shares = get_multi_infos("share_content")
    return get_random_from_list(shares)


def get_multi_infos(str):
    users = os.getenv(str)
    if len(users) != 0:
        return users.split('|')
    return {}


def get_random_from_list(list):
    if len(list) != 0:
        return random.choice(list)
    return "_"


share_content = get_random_share_content()
comment_content = get_random_comment_content()
ups = get_multi_infos("ups")
db_host = getHost()
selenium_url = "http://" + getHost() + ":5555"

if __name__ == '__main__':
    print(db_host)
    print(selenium_url)
