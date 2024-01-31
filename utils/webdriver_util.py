from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import globals



class ElementUtil(object):
    def get_element_by_xpath(bro, chains, path):
        """
        获取element的通用方法
        :param bro:
        :param chains:
        :param path:
        :return:
        """
        return WebDriverWait(bro, 10).until(EC.element_to_be_clickable((By.XPATH, path)))

    def get_elementArr_by_xpath(bro, chains, path):
        return WebDriverWait(bro, 10).until(EC.presence_of_all_elements_located((By.XPATH, path)))

    def is_xpath_exist(bro, chains, path):
        try:
            WebDriverWait(bro, 5).until(EC.element_to_be_clickable((By.XPATH, path)))
            return True
        except:
            return False

    def wait_to_go(bro, timeout=10):
        WebDriverWait(bro, timeout).until(EC.new_window_is_opened)

def local_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  # 以无头模式运行Chrome
    chrome_options.add_argument("--no-sandbox")  # 取消沙盒模式
    chrome_options.add_argument("--disable-gpu")  # 取消GPU
    chrome_options.add_argument("--disable-extensions")  # 禁用插件加载
    chrome_options.add_argument("--disable-software-rasterizer")  # 禁用软件光栅化器
    chrome_options.add_argument('lang=zh_CN.UTF-8')
    chrome_options.add_argument('--enable-javascript')
    chrome_options.add_argument("--start-minimized")
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/115.0.5790.110 Safari/537.36')  # 替换User-Agent
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    s = Service(r"./lib/chromedriver.exe")
    bro = webdriver.Chrome(service=s, chrome_options=chrome_options, options=option)
    chains = ActionChains(bro)
    return bro, chains


def online_driver():
    """
        初始化Selenium信息———— 此版本用于生成Cookie，所以浏览器去掉无头模式
        :return:
        """
    # 设置浏览器信息
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  # 以无头模式运行Chrome
    chrome_options.add_argument("--no-sandbox")  # 取消沙盒模式
    chrome_options.add_argument("--disable-gpu")  # 取消GPU
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("blink-settings=imagesEnabled=false")  # 配置不加载图片
    chrome_options.add_argument("--disable-extensions")  # 禁用插件加载
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

def init_webdriver():

    if globals.DRIVER_VERSION == 'Local':
        return local_driver()
    if globals.DRIVER_VERSION == 'Online':
        return online_driver()
    # 默认本地驱动
    return local_driver()