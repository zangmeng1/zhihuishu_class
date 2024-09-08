import datetime
import os
import time
from yidun import yidun
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

def print_true(msg:str):#关键性操作信息
    print('\033[92m'+str(msg)+'\033[0m')


def print_error(msg):#意外信息
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
    time.sleep(1)
    while True:
        try:
            named=driver.find_element(By.XPATH, "//span[@class='user-logo_name']")
            name=named.get_attribute('textContent')#提取标签对中文本
            if name !='':#防止网页还没刷新
                break
        except:
            #防止易盾过多尝试
            yidun_tip = driver.find_element(By.XPATH, "//span[@class='yidun_tips__text yidun-fallback__tip']")
            yidun_tip_msg = yidun_tip.get_attribute('textContent')  # 提取标签对中文本
            if yidun_tip_msg=='失败过多，点此重试':
                yidun_tip=driver.find_element(By.XPATH, "//div[@aria-live='polite']")
                yidun_tip.click()
            else:
                if not error_printed:
                    error_printed=True
                    write_log('网易易盾拦截登录')
                print_error("网易易盾拦截,正在尝试破解，多次失败请手动验证！")
                yidun(driver)

            time.sleep(0.5)
    print_true(f"登陆成功，欢迎你#{name}#")
    write_log(f"用户:{name}，登录成功")


def get_class():
    print("开始定位课程")
    # 获取 多个 线段
    all_class_line = driver.find_elements(By.XPATH,f"//div[@class='item-left-course']")
    time.sleep(3)
    # 尝试点击多个线段
    # for line in all_class_line:
    #     print(line.text)
    print(all_class_line[0].text)

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
    input("调试用暂停")
    get_class()


