from datetime import datetime
import random
import time

def deal_time(sj):
    if "小时" in sj or "分钟" in sj or "刚刚" in sj:
        return datetime.time.strftime("%Y-%m-%d", time.localtime(time.time()))
    if len(sj) == 5:
        return '2023-' + sj
    return sj;


def random_sleep(start=1, end=5):
    # 生成随机的睡眠时间，范围为1到5秒
    sleep_time = random.randint(start, end)
    # print("休眠时间" +str(sleep_time))
    # 进行睡眠操作
    time.sleep(sleep_time)




if __name__ == '__main__':
    print(datetime.now())
    random_sleep()
    print(datetime.now())
    random_sleep()
    print(datetime.now())
    random_sleep()
    print(datetime.now())
    random_sleep()
    print(datetime.now())

