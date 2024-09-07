import datetime
import logging
import os
import time
from email._header_value_parser import get_attribute
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

#登录接口
#https://passport.zhihuishu.com/login?service=https://onlineservice-api.zhihuishu.com/gateway/f/v1/login/gologin#signin

log_path=f'./log/{datetime.date.today()}.txt'
error_printed=False

def print_true(msg:str):
    print('\033[92m'+str(msg)+'\033[0m')

def print_error(msg):
    print('\033[31m' + str(msg) + '\033[0m')

def write_log(msg):
    custom_date = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
    with open(log_path, "a") as file:
        file.write(f"[{custom_date}]{msg}\n")

def login(username, password):
    global error_printed
    print("开始登录智慧树")
    driver.get("https://passport.zhihuishu.com/login?service=https://onlineservice-api.zhihuishu.com/gateway/f/v1/login/gologin#signin")
    print("等待输入账密登录")
    time.sleep(3)
    driver.find_element("name", "username").send_keys(username)
    driver.find_element("name", "password").send_keys(password)
    print(username, password,"信息输入完成")
    print("等待提交登录信息")
    time.sleep(1)
    # 使用XPath定位元素
    element = driver.find_element(By.XPATH, "//span[@class='wall-sub-btn']")
    driver.execute_script("imgSlidePop(ImgSlideCheckModule.SignUpError3);", element)
    print("提交登录完成")
    write_log("提交登录请求完成")
    while True:
        try:
            named=driver.find_element(By.XPATH, "//span[@class='user-logo_name']")
            name=named.get_attribute('textContent')#提取标签对中文本
            if name !='':#防止网页还没刷新
                break
        except:
            if not error_printed:
                print_error("易盾拦截，请手动验证！")
                error_printed=True
                write_log("网易易盾拦截登录")
            print('.',end="")
            time.sleep(3)
    print_true(f"登陆成功，欢迎你#{name}#")
    write_log(f"用户:{name}，登录成功")

if __name__ == "__main__":
    username='17669671576'
    password= 'Aa316774204'
    #初始化日志文件
    if not os.path.exists(log_path):
        with open(log_path, 'w', encoding='utf-8') as file:
            file.write("")
    write_log("程序启动")
    # 初始化 Edge WebDriver
    driver = webdriver.Edge()
    login(username, password)




