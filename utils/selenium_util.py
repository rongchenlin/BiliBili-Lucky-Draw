from selenium import webdriver
from selenium.webdriver import ActionChains
import globals

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions


# def init_webdriver():
#     """
#     初始化Selenium信息———— 此为服务器版本，用于部署使用
#     :return:
#     """
#     # 设置浏览器信息
#     chrome_options = webdriver.ChromeOptions()
#     # chrome_options.add_argument("--headless")  # 以无头模式运行Chrome
#     chrome_options.add_argument("--no-sandbox")  # 取消沙盒模式
#     chrome_options.add_argument('lang=zh_CN.UTF-8')
#     chrome_options.add_argument(
#         '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
#         'Chrome/101.0.4951.64 Safari/537.36')  # 替换User-Agent
#     driver = webdriver.Remote(
#         command_executor=globals.selenium_url,
#         options=chrome_options
#     )
#     chains = ActionChains(driver)
#     return driver, chains


def init_webdriver():
    """
    作用和上面的相同，都是用于初始化Selenium
    此段代码用于在本地调试使用，注意：请根据Readme.md文档到指定位置下载与当前Chrome浏览器匹配的chromedriver.exe
    :return:
    """
    chrome_options = Options()
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    s = Service(r"./chromedriver.exe")
    bro = webdriver.Chrome(service=s, chrome_options=chrome_options, options=option)
    chains = ActionChains(bro)
    return bro, chains


