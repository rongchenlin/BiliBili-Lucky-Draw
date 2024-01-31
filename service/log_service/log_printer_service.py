import logging
import time
import os


class MyLogger(object):

    def __init__(self, name=None):
        self.name = name
        # ①创建一个记录器
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel("INFO")  # 设置日志级别为 'level'，即只有日志级别大于等于'level'的日志才会输出
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")  # 创建formatter
        # ②创建屏幕-输出到控制台，设置输出等级
        self.streamHandler = logging.StreamHandler()
        self.streamHandler.setLevel("INFO")
        # ③创建log文件，设置输出等级
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 根目录
        time_now = time.strftime('%Y_%m_%d_%H', time.localtime()) + '_err' + '.log'  # log文件命名：2022_04_02_21.log
        self.fileHandler = logging.FileHandler(os.path.join('./', "Log", time_now ), 'a', encoding='utf-8')
        self.fileHandler.setLevel("ERROR")
        # ④用formatter渲染这两个Handler
        self.streamHandler.setFormatter(self.formatter)
        self.fileHandler.setFormatter(self.formatter)
        # ⑤将这两个Handler加入logger内
        self.logger.addHandler(self.streamHandler)
        self.logger.addHandler(self.fileHandler)

    def getLogger(self):
        return self.logger

    def print_run_time(self, name, begin_time, end_time):
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
