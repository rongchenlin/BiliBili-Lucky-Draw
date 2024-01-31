import time

from selenium.webdriver import ActionChains, Keys

from service.log_service.log_printer_service import MyLogger
from service.login_service.login_service import LoginService
from utils.time_util import random_sleep
from utils.webdriver_util import init_webdriver, ElementUtil
from utils import globals

mylogger = MyLogger('remove_msg.py').getLogger()


class RemoveMsgService(object):
    """
    多用户转发模式
    """

    def __init__(self, user_id, cnt, bro, chains):
        self.user_id = user_id
        self.cnt = cnt
        self.bro = bro
        self.chains = chains
        mylogger.error('移除通知信息!')

    def do_remove(self):
        base_url = 'https://message.bilibili.com/?spm_id_from=333.1007.0.0#/whisper'
        try:
            # bro, chains = init_webdriver()
            # LoginService(self.bro, self.chains, self.user_id).login_by_cookie()
            self.bro.get(base_url)
            first_dyn_element = ElementUtil.get_element_by_xpath(self.bro, self.chains,'//*[@id="link-message-container"]/div[1]/div[2]/div[2]/div[1]/div/div/div[4]/div[2]/div[1]/div[1]')
            # 创建ActionChains对象
            actions = ActionChains(self.bro)
            actions.move_to_element(first_dyn_element).perform()
            # 循环滚动和点击
            scroll_distance = 2
            for i in range(self.cnt):  # 你可以根据需要设置循环次数
                # 模拟滚轮滚动
                ActionChains(self.bro).send_keys(Keys.ARROW_DOWN * scroll_distance).perform()
                # 等待一段时间，确保页面有足够的时间进行滚动
                time.sleep(1)
                ActionChains(self.bro).click().perform()
                random_sleep(start=1, end=5)
        except:
            mylogger.error("[移除通知信息流程 出错]")
        finally:
            print(1)

if __name__ == '__main__':
    RemoveMsgService(globals.my_user_id).do_remove()
