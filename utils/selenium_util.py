from selenium import webdriver
from selenium.webdriver import ActionChains
import globals


def visit_url(bro):
    return bro

def init_webdriver():
    """
    初始化Selenium信息
    :return:
    """
    # 设置浏览器信息
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  # 以无头模式运行Chrome
    chrome_options.add_argument("--no-sandbox")  # 取消沙盒模式
    chrome_options.add_argument('lang=zh_CN.UTF-8')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/101.0.4951.64 Safari/537.36')  # 替换User-Agent
    driver = webdriver.Remote(
        command_executor=globals.selenium_url,
        options=chrome_options
    )
    chains = ActionChains(driver)
    return driver, chains
