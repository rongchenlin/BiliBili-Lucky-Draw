import time
from datetime import datetime

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from dao.draw_dynamic_dao import DrawDynamicDao
from dao.init_db import init_db
from dao.statistics_dao import StatisticsDao
from service.log_service.log_printer_service import MyLogger
from service.login_service.login_service import LoginService
from service.notify_service.notify_service import NotifyService
from utils.ip_util import remove_query_string
from utils.time_util import random_sleep
from utils.webdriver_util import init_webdriver, ElementUtil
from utils import globals
mylogger = MyLogger('SearchDynamicByUps.py').getLogger()


class SearchDynamicByUps(object):

    def __init__(self, user_id):
        self.count = 0
        self.user_id = user_id
        self.search_note = ""
        db = init_db()
        self.draw_dynamic_dao = DrawDynamicDao(db)
        self.statistics_dao = StatisticsDao(db)


    def searchFromFiftyUps(self, bro, chains):
        """
        up主：你的工具人老公
        up主链接：https://space.bilibili.com/100680137/dynamic
        来源：https://space.bilibili.com/100680137/dynamic
        :return:
        """
        base_url = 'https://space.bilibili.com/100680137/dynamic'
        try:
            # 前往主页
            bro.get(base_url)
            bro.refresh()
            pathOne = '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/div/div[2]'
            first_dyn_element = ElementUtil.get_element_by_xpath(bro, chains, pathOne)
            first_dyn_element.click()
            ElementUtil.wait_to_go(bro)
            bro.switch_to.window(bro.window_handles[-1])
            bro.refresh()
            random_sleep()
            # 到达动态列表页
            source_url = bro.current_url
            # 获取链接所在的块
            all_links_ele = ElementUtil.get_element_by_xpath(bro, chains, '/html/body/div[3]/div/div[3]/div[1]/div[4]/div')
            # 在<div>元素下找到所有<a>标签元素
            link_elements = all_links_ele.find_elements_by_xpath(".//a")
            links = [element.get_attribute("href") for element in link_elements]
            self.dynLinks_to_db(links, remove_query_string(source_url), "你的工具人老公")
        except Exception as e:
            mylogger.error("[searchFromFiftyUps 从“你的工具人老公”查找抽奖动态 出错 %s]" % e, exc_info=True)
            NotifyService().fangtang_msg_push_by_content(title="“你的工具人老公”查找抽奖动态出错", content='从“你的工具人老公”查找抽奖动态 出错')

    def searchFromBigFish(self, bro, chains):
        """
        up主：_大锦鲤_
        up主链接：https://space.bilibili.com/226257459/dynamic
        :return:
        """
        base_url = 'https://space.bilibili.com/226257459/dynamic'
        try:
            bro.get(base_url)
            bro.refresh()
            pathOne = '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[1]/div/div/div[3]/div/div/div/div'
            base_link_element = ElementUtil.get_element_by_xpath(bro, chains, pathOne)
            base_link_element.click()
            WebDriverWait(bro, 10).until(EC.new_window_is_opened)
            bro.switch_to.window(bro.window_handles[-1])
            bro.refresh()
            random_sleep()
            # 到达动态列表页
            source_url = bro.current_url
            # 获取这些<a>标签的href属性值
            elements = ElementUtil.get_elementArr_by_xpath(bro, chains, '//a[contains(text(), "网页链接")]')
            links = [element.get_attribute("href") for element in elements]
            filtered_links = [link for link in links if "mall.bilibili" not in link]
            self.dynLinks_to_db(filtered_links, remove_query_string(source_url), "_大锦鲤_")
        except Exception as e:
            mylogger.error("[searchFromBigFish 从“_大锦鲤_”查找抽奖动态 出错 %s]" % e, exc_info=True)
            NotifyService().fangtang_msg_push_by_content(title="“_大锦鲤_”查找抽奖动态出错", content='从“_大锦鲤_”查找抽奖动态 出错')

    def searchFromCarcinus_(self, bro, chains):
        """
        up主：Carcinus_
        up主链接：https://space.bilibili.com/27332255/dynamic
        :return:
        """
        base_url = 'https://space.bilibili.com/27332255/dynamic'
        try:
            bro.get(base_url)
            bro.refresh()
            pathOne = '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[1]/div/div/div[3]/div/div/div/div/div[1]'
            base_link_element = ElementUtil.get_element_by_xpath(bro, chains, pathOne)
            base_link_element.click()
            WebDriverWait(bro, 10).until(EC.new_window_is_opened)
            bro.switch_to.window(bro.window_handles[-1])
            bro.refresh()
            random_sleep()
            # 到达动态列表页
            source_url = bro.current_url
            # 获取这些<a>标签的href属性值
            elements = ElementUtil.get_elementArr_by_xpath(bro, chains, '//a[contains(text(), "LINK")]')
            links = [element.get_attribute("href") for element in elements]
            self.dynLinks_to_db(links, remove_query_string(source_url), "Carcinus_")
        except Exception as e:
            mylogger.error("[searchFromCarcinus_ 从“Carcinus_”查找抽奖动态 出错 %s]" % e, exc_info=True)
            NotifyService().fangtang_msg_push_by_content(title="“Carcinus_”查找抽奖动态出错", content='从“Carcinus_”查找抽奖动态 出错')

    def searchFromSmile(self, bro, chains):
        """
        up主：闻不着味
        up主链接：https://space.bilibili.com/280025263/dynamic
        :return:
        """
        base_url = 'https://space.bilibili.com/280025263/dynamic'
        try:
            bro.get(base_url)
            bro.refresh()
            pathOne = self.find_first_ele(bro, chains)
            base_link_element = ElementUtil.get_element_by_xpath(bro, chains, pathOne)
            base_link_element.click()
            WebDriverWait(bro, 10).until(EC.new_window_is_opened)
            bro.switch_to.window(bro.window_handles[-1])
            bro.refresh()
            random_sleep()
            # 到达动态列表页
            source_url = bro.current_url
            # 获取这些<a>标签的href属性值
            elements = ElementUtil.get_elementArr_by_xpath(bro, chains, '//a[contains(text(), "http")]')
            links = [element.get_attribute("href") for element in elements]
            self.dynLinks_to_db(links, remove_query_string(source_url), "闻不着味")
        except Exception as e:
            mylogger.error("[searchFromSmile 从“闻不着味”查找抽奖动态 出错 %s]" % e, exc_info=True)
            NotifyService().fangtang_msg_push_by_content(title="“闻不着味”查找抽奖动态出错", content='从“闻不着味”查找抽奖动态 出错')

    def find_first_ele(self, bro, chains):
        pathOnes = [
            '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/div/div[1]'
            '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/div',
            '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/div/div[2]',
            '//*[@id="page-dynamic"]/div[1]/div/div[1]/div[1]/div/div[2]/div[3]/div/div[3]/div[2]/div/div[1]',
        ]
        for pathOne in pathOnes:
            if ElementUtil.is_xpath_exist(bro, chains,pathOne):
                return pathOne
        return None;

    def dynLinks_to_db(self, dynLinks, source, note):
        cnt = 0
        break_flag = 0
        ignore_links = self.get_ignore_link()
        for link in dynLinks:
            try:
                # 跳过非抽奖动态
                for ign_lnk in ignore_links:
                    if ign_lnk in link:
                        break_flag = 1
                if break_flag == 1:
                    break_flag = 0
                    continue
                break_flag = 0
                # 跳过已经入库的
                if len(self.draw_dynamic_dao.query_by_dyn_url(remove_query_string(link))) == 0:
                    self.draw_dynamic_dao.insert(remove_query_string(link), source, note)
                    cnt = cnt + 1
            except Exception as e:
                mylogger.error("[dynLinks_to_db 动态插入数据库 出错 %s]" % e, exc_info=True)
        self.count = self.count + cnt
        self.search_note = self.search_note + note + ":" + str(cnt) + ";  "

    def get_ignore_link(self):
        links = globals.ignore_link
        if len(links) != 0:
            return links.split('|')
        return {}

    def init_search(self):
        bro = None
        try:
            bro, chains = init_webdriver()
            LoginService(bro, chains, self.user_id).login_by_cookie()
            if "你的工具人老公" in globals.ups:
                self.searchFromFiftyUps(bro, chains)
            if "_大锦鲤_" in globals.ups:
                self.searchFromBigFish(bro, chains)
            if "Carcinus_" in globals.ups:
                self.searchFromCarcinus_(bro, chains)
            if "闻不着味" in globals.ups:
                self.searchFromSmile(bro, chains)
            # 统计入库
            self.statistics_dao.insert("", "搜索到的抽奖动态条数为: " + str(self.count), self.search_note)
        except:
            mylogger.error("[搜索抽奖动态列表主流程 出错]")
        finally:
            bro.quit()


if __name__ == '__main__':
    SearchDynamicByUps().init_search()
