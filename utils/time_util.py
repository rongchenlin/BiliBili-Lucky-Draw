import datetime
import time

def deal_time(sj):
    if "小时" in sj or "分钟" in sj or "刚刚" in sj:
        return datetime.time.strftime("%Y-%m-%d", time.localtime(time.time()))
    if len(sj) == 5:
        return '2023-' + sj
    return sj;