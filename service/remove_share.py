import time

from selenium.webdriver import ActionChains, Keys

from dao.init_db import init_db
from dao.shared_url_dao import SharedUrlDao
from service.log_service.log_printer_service import MyLogger
from service.login_service.login_service import LoginService
from utils.time_util import random_sleep
from utils.webdriver_util import init_webdriver, ElementUtil
from utils import globals

mylogger = MyLogger('remove_share.py').getLogger()


class RemoveShareService(object):
    """
    多用户转发模式
    """

    def __init__(self, user_id, cnt=None, bro=None, chains=None):
        self.user_id = user_id
        self.db = init_db()
        self.sharedUrlDao = SharedUrlDao(self.db)
        if bro is None:
            self.bro, self.chains = init_webdriver()
            LoginService(self.bro, self.chains, self.user_id).login_by_cookie()
        else:
            self.bro = bro
            self.chains = chains
        self.cnt = cnt
        mylogger.error('移除通知信息!')

    def get_expired_url(self, scroll_cnt):
        base_url = 'https://space.bilibili.com/385649497/dynamic'
        try:
            self.bro.get(base_url)
            scroll_path = '//*[@id="page-dynamic"]'
            first_dyn_element = ElementUtil.get_element_by_xpath(self.bro, self.chains, scroll_path)
            # 创建ActionChains对象
            actions = ActionChains(self.bro)
            actions.move_to_element(first_dyn_element).perform()
            # 循环滚动和点击
            scroll_distance = 400
            for i in range(scroll_cnt):  # 你可以根据需要设置循环次数
                # 模拟滚轮滚动
                ActionChains(self.bro).send_keys(Keys.ARROW_DOWN * scroll_distance).perform()
                random_sleep(start=1, end=4)

            div_elements = self.bro.find_elements_by_xpath("//div[@class='bili-dyn-more__menu__item']")
            # 遍历每个<div>元素，检查是否包含data-params属性，并提取dynamic_id的值
            for div_element in div_elements:
                class_attribute = div_element.get_attribute("class")
                data_params_attribute = div_element.get_attribute("data-params")
                # 检查是否包含class="bili-dyn-more__menu__item"以及data-params属性
                if "bili-dyn-more__menu__item" in class_attribute and data_params_attribute:
                    # 提取dynamic_id的值
                    dynamic_id_start = data_params_attribute.find('"dynamic_id"') + len('"dynamic_id"') + 1
                    dynamic_id_end = data_params_attribute.find('"', dynamic_id_start + 1)
                    dynamic_id_value = data_params_attribute[dynamic_id_start + 1:dynamic_id_end].strip()
                    if dynamic_id_value != '':
                        url = 'https://www.bilibili.com/opus/' + dynamic_id_value
                        self.sharedUrlDao.insert_sharedUrl(self.user_id, url)
        except Exception as e:
            mylogger.error("[获取过期动态流程 出错 %s]" % e, exc_info=True)

    def do_remove(self):
        """
        批量删除过期url
        :return:
        """
        try:
            datas = self.sharedUrlDao.query_sharedUrls_limit(self.user_id, '0', self.cnt)
            for data in datas:
                lucky_dynamic_url = data['dyn_url']
                self.remove_one(lucky_dynamic_url)
        except:
            mylogger.error("[do_remove 批量删除过期url 出错]")

    def remove_one(self, lucky_dynamic_url):
        """
        移除一个过期url
        :param lucky_dynamic_url: 需要进行转发的抽奖动态的URL
        :return:
        """
        try:
            self.bro.get(lucky_dynamic_url)
            self.bro.refresh()
            ElementUtil.wait_to_go(self.bro)
            self.click_delete(self.bro, self.chains)
            random_sleep()
            # 回填状态
            self.sharedUrlDao.update_sharedUrl(self.user_id, lucky_dynamic_url, '1')
        except Exception as e:
            mylogger.error("remove_one 移除一个过期url 出错url : " + lucky_dynamic_url)
        finally:
            mylogger.info('移除一个过期url--执行结束')

    def click_delete(self, bro, chains):
        """
        点赞
        :param bro:
        :param chains:
        :return:
        """
        try:
            find_path = '//*[@id="app"]/div[3]/div/div/div[1]/div[2]/div[4]/div'
            find_path_ele = ElementUtil.get_element_by_xpath(bro, chains, find_path)
            chains.click(find_path_ele).perform()
            random_sleep(start=1, end=3)

            delete_path = '//*[@id="app"]/div[3]/div/div/div[1]/div[2]/div[4]/div/div'
            delete_path_ele = ElementUtil.get_element_by_xpath(bro, chains, delete_path)
            chains.click(delete_path_ele).perform()
            random_sleep(start=1, end=3)

            do_delete_path = '/html/body/div[4]/div[2]/div[4]/button[2]'
            do_delete_ele = ElementUtil.get_element_by_xpath(bro, chains, do_delete_path)
            chains.click(do_delete_ele).perform()
            random_sleep(start=1, end=3)

        except Exception as e:
            mylogger.error("[click_like 点击“删除” 出错 %s]" % e, exc_info=True)
            raise

    def quilt_bro(self):
        self.bro.quit()

    def start_remove_service(self):
        if globals.is_remove == 'Y':
            self.do_remove()
            self.get_expired_url(10)
            self.quilt_bro()
        else:
            mylogger.error("移除过期url开关未打开")
