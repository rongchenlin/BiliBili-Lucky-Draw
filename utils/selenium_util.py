from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


def init_webdriver():

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  # 以无头模式运行Chrome
    chrome_options.add_argument("--no-sandbox")  # 取消沙盒模式
    chrome_options.add_argument('lang=zh_CN.UTF-8')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36')  # 替换User-Agent
    driver = webdriver.Remote(
        command_executor='http://123.56.224.232:5555',
        options=chrome_options
    )
    chains = ActionChains(driver)
    return driver, chains

def init_webdriver2():

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  # 以无头模式运行Chrome
    chrome_options.add_argument("--no-sandbox")  # 取消沙盒模式
    chrome_options.add_argument('lang=zh_CN.UTF-8')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36')  # 替换User-Agent
    driver = webdriver.Remote(
        command_executor='http://123.56.224.232:5555',
        options=chrome_options
    )
    chains = ActionChains(driver)
    return driver, chains

def init_webdriver3():

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  # 以无头模式运行Chrome
    chrome_options.add_argument("--no-sandbox")  # 取消沙盒模式
    chrome_options.add_argument('lang=zh_CN.UTF-8')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36')  # 替换User-Agent
    driver = webdriver.Remote(
        command_executor='http://x.x.x.x:5555',
        options=chrome_options
    )
    chains = ActionChains(driver)
    return driver, chains

def init_webdriver4():

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  # 以无头模式运行Chrome
    chrome_options.add_argument("--no-sandbox")  # 取消沙盒模式
    chrome_options.add_argument('lang=zh_CN.UTF-8')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36')  # 替换User-Agent
    driver = webdriver.Remote(
        command_executor='http://x.x.x.x:5555',
        options=chrome_options
    )
    chains = ActionChains(driver)
    return driver, chains

def is_xpath_exist(bro, xpath):
    try:
        bro.find_element(By.XPATH, xpath)
        return True
    except:
        return False