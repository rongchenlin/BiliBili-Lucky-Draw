import time
from datetime import datetime
from service.log_service.log_printer_service import MyLogger
from utils.ip_util import get_host_ip, get_partContent_from_lick
from utils.time_util import random_sleep
from utils.webdriver_util import ElementUtil

mylogger = MyLogger('share_one_dynamic.py').getLogger()


class DynamicShareBase(object):

    def __init__(self):
        # 公有属性，可以在类外部访问
        self.upId = None
        self.upUrl = None
        self.share_url = None
        self.status = 1
        self.machine_ip = None
        self.share_time = None
        self.share_status = 1
        self.user_id = None

    def share_one(self, bro, chains, lucky_dynamic_url, share_content, comment_content):
        """
        提供需要转发的抽奖动态URL，然后“执行状态、up主的ID、up主的主页URL”等信息
        :param bro:
        :param chains:
        :param lucky_dynamic_url: 需要进行转发的抽奖动态的URL
        :return:
        """
        try:
            bro.get(lucky_dynamic_url)
            bro.refresh()
            ElementUtil.wait_to_go(bro)
            # 新版转旧版本
            self.to_old_version(bro, chains)
            # 点击关注
            self.click_follow(bro, chains)
            random_sleep()
            # 点赞
            self.click_like(bro, chains)
            random_sleep()
            # 预约抽奖
            self.click_reserve(bro, chains)
            random_sleep()
            # 评论
            self.commit_comment(bro, chains, comment_content)
            random_sleep()
            # 移动到“分享”按钮, 点击“转发”
            self.click_share(bro, chains, share_content)
            random_sleep()
            # 回填状态
            self.share_status = 0
            self.status = 0
            self.share_url = lucky_dynamic_url
        except Exception as e:
            mylogger.error("share_one 转发单条动态主流程 出错url : " + lucky_dynamic_url)
        finally:
            self.share_time = str(datetime.now())
            self.machine_ip = get_host_ip()
            mylogger.info('单条动态转发--执行结束')

    def click_follow(self, bro, chains):
        """
        点击关注，并且返回相关的up主信息
        :param bro:
        :param chains:
        :return:
        """
        try:
            username = ElementUtil.get_element_by_xpath(bro, chains,
                                                        '//*[@id="app"]/div[3]/div/div/div[1]/div[2]/div[1]/span')
            # 跳转到新页面（up主的主页）
            username.click()
            ElementUtil.wait_to_go(bro)
            bro.switch_to.window(bro.window_handles[-1])
            bro.refresh()
            random_sleep()
            current_url = bro.current_url
            user_id = get_partContent_from_lick(current_url)
            self.upId = str(user_id)
            self.upUrl = 'https://space.bilibili.com/' + self.upId
            # 是否包含“已关注”标签
            has_followd = ElementUtil.get_element_by_xpath(bro, chains,
                                                           '//*[@id="app"]/div[1]/div[1]/div[2]/div[4]/div[1]/div')
            if "已关注" not in has_followd.get_attribute('innerText'):
                do_follow_btn = ElementUtil.get_element_by_xpath(bro, chains,
                                                                 '//*[@id="app"]/div[1]/div[1]/div[2]/div[4]/span')
                chains.click(do_follow_btn).perform()
            bro.close()
            bro.switch_to.window(bro.window_handles[-1])
        except Exception as e:
            mylogger.error("[click_follow 点击“关注” 出错 %s]" % e, exc_info=True)
            # 将异常传递给上一级函数
            raise

    def click_like(self, bro, chains):
        """
        点赞
        :param bro:
        :param chains:
        :return:
        """
        try:
            path = '//*[@id="app"]/div[3]/div[2]/div/div[1]/div[1]'
            like_btn_old = ElementUtil.get_element_by_xpath(bro, chains, path)
            chains.click(like_btn_old).perform()
        except Exception as e:
            mylogger.error("[click_like 点击“点赞” 出错 %s]" % e, exc_info=True)
            raise


    def click_reserve(self, bro, chains):
        """
        预约抽奖
        :param bro:
        :param chains:
        :return:
        """
        try:
            reserve_path = '//*[@id="app"]/div[3]/div[1]/div[1]/div/div[3]/div/div/div[3]/div/div/div[2]/button'
            if ElementUtil.is_xpath_exist(bro, chains, reserve_path):
                reserve_btn = ElementUtil.get_element_by_xpath(bro, chains, reserve_path)
                chains.click(reserve_btn).perform()
        except Exception as e:
            mylogger.error("[click_like 点击“预约抽奖” 出错 %s]" % e, exc_info=True)
            raise

    def commit_comment(self, bro, chains, comment_content):
        """
        评论
        :param comment_content:
        :param bro:
        :param chains:
        :return:
        """
        try:
            comment_old = ElementUtil.get_element_by_xpath(bro, chains,
                '//*[@id="app"]/div[3]/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div/div[1]/div[2]/div')
            chains.click(comment_old).perform()
            comment_xx_path = '//*[@id="app"]/div[3]/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div/div[1]/div[2]/div/textarea'
            comment_cont = ElementUtil.get_element_by_xpath(bro, chains,comment_xx_path)
            comment_cont.send_keys("" + str(comment_content))
            commit_btn_old = ElementUtil.get_element_by_xpath(bro, chains,
                            '//*[@id="app"]/div[3]/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div[2]/div[1]/div/div[2]/div[2]/div')
            chains.click(commit_btn_old).perform()
        except Exception as e:
            mylogger.error("[commit_comment 点击“评论” 出错 %s]" % e, exc_info=True)
            raise

    def click_share(self, bro, chains, share_content):
        """
        执行转发动态
        :param bro:
        :param chains:
        :return:
        """
        try:
            share_btn_old = ElementUtil.get_element_by_xpath(bro, chains,
                                                    '//*[@id="app"]/div[3]/div[2]/div/div[1]/div[2]')
            chains.click(share_btn_old).perform()
            share_text_old = ElementUtil.get_element_by_xpath(bro, chains,
                        '/html/body/div[4]/div[2]/div[1]/div/div[3]/div[1]/div')
            share_text_old.send_keys(share_content)
            do_share_btn_old = ElementUtil.get_element_by_xpath(bro, chains,
                            '/html/body/div[4]/div[2]/div[1]/div/div[5]/div[2]/div[2]')
            chains.click(do_share_btn_old).perform()
            random_sleep()
        except Exception as e:
            mylogger.error("[click_share 点击“分享” 出错 %s]" % e, exc_info=True)
            raise

    def to_old_version(self, bro, chains):
        """
        新版转旧版
        :param bro:
        :param chains:
        :return:
        """
        if ElementUtil.is_xpath_exist(bro, chains, '//*[@id="app"]/div[4]/div[3]/div/div[2]/div[1]') is True:
            to_old_btn = ElementUtil.get_element_by_xpath(bro, chains,
                                                          '//*[@id="app"]/div[4]/div[3]/div/div[2]/div[1]')
            to_old_btn.click()
            ElementUtil.wait_to_go(bro)
