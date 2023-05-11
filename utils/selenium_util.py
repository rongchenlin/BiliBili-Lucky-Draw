
from selenium import webdriver
from selenium.webdriver import ActionChains
# 实现规避检测
from selenium.webdriver import ChromeOptions
# 实现无可视化界面
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def init_webdriver():
    # # 实现无可视化界面的操作
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # 实现规避检测的变量：option
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 实现让selenium规避被检测到的风险
    s = Service(r"./chromedriver.exe")
    # bro = webdriver.Chrome(service=s, chrome_options=chrome_options, options=option)
    bro = webdriver.Chrome(service=s)
    chains = ActionChains(bro)
    return bro, chains

def is_xpath_exist(bro, xpath):
    try:
        bro.find_element(By.XPATH, xpath)
        return True
    except:
        return False