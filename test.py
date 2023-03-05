
import requests
from cron_lite import cron_task, start_all
import time
import schedule


# @cron_task("* * * * * 0/2")
def event1():
    print("event1", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    time.sleep(3)
    print("event1 done", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

@cron_task("38 23 * * * 35")
def event2():
    print("event2", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    time.sleep(10)
    print("event2 done", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))


def job():
    print("I'm working...")





if __name__ == '__main__':
    # start_all()
    # input()
    schedule.every().day.at("23:45").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

    # url = 'https://sctapi.ftqq.com/SCT172323TZn2oLYosf0TJY80XSH7KN29R.send'
    # data = {
    #     'title': '测试title',
    #     'desp': '测试desp',
    #     'short': '测试short'
    # }
    # r = requests.post(url, data)
    # print(r.text)