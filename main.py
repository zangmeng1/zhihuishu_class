import datetime
import json
import os
import time

import pyautogui
from selenium.webdriver import Keys

from yidun import yidun
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
#登录接口
#https://passport.zhihuishu.com/login?service=https://onlineservice-api.zhihuishu.com/gateway/f/v1/login/gologin#signin

log_path=f'./log/{datetime.date.today()}.txt'


def print_true(msg:str):#关键性操作信息
    print('\033[92m'+str(msg)+'\033[0m')


def print_error(msg):#意外信息
    print('\033[31m' + str(msg) + '\033[0m')


def write_log(msg):
    custom_date = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
    with open(log_path, "a") as file:
        file.write(f"[{custom_date}]{msg}\n")


class zhihuishu_class:
    def __init__(self):
        # 初始化日志文件
        if not os.path.exists(log_path):
            with open(log_path, 'w', encoding='utf-8') as file:
                file.write("")
        print("——————正在初始化浏览器——————")
        # 初始化 Edge WebDriver
        driver = webdriver.Edge()
        self.driver = driver
        self.error_printed = False#错误信息是否已打印


    def login(self,username, password):
        self.username=username
        print("开始登录智慧树")
        self.driver.get("https://passport.zhihuishu.com/login?service=https://onlineservice-api.zhihuishu.com/gateway/f/v1/login/gologin#signin")
        print("等待输入账密登录")
        time.sleep(3)
        self.driver.find_element("name", "username").send_keys(username)
        self.driver.find_element("name", "password").send_keys(password)
        print(username, password,"信息输入完成")
        print("等待提交登录信息")
        time.sleep(1)
        # 使用XPath定位元素
        element = self.driver.find_element(By.XPATH, "//span[@class='wall-sub-btn']")
        self.driver.execute_script("imgSlidePop(ImgSlideCheckModule.SignUpError3);", element)
        print("提交登录完成")
        write_log("提交登录请求完成")
        time.sleep(1)
        while True:
            try:
                named=self.driver.find_element(By.XPATH, "//span[@class='user-logo_name']")
                name=named.get_attribute('textContent')#提取标签对中文本
                self.error_printed=True
                if name !='':#防止网页还没刷新
                    break
            except:
                #易盾过多尝试会产生二次验证
                yidun_tip = self.driver.find_element(By.XPATH, "//span[@class='yidun_tips__text yidun-fallback__tip']")
                yidun_tip_msg = yidun_tip.get_attribute('textContent')  # 提取标签对中文本
                if yidun_tip_msg=='失败过多，点此重试':
                    yidun_tip=self.driver.find_element(By.XPATH, "//div[@aria-live='polite']")
                    yidun_tip.click()
                else:
                    print_error("网易易盾拦截,正在尝试破解,多次尝试请手动验证")
                    yidun(self.driver)
                    if not self.error_printed:#log只打印一次
                        self.error_printed=True
                        write_log('**WARRING**网易易盾拦截登录')
                    else:#第二次自动行为将等待时间延长3s，用户可人为干预
                        time.sleep(3)
                time.sleep(0.5)
        print_true(f"#{username}#登陆成功")
        write_log(f"#{username}#，登录成功")


    def get_class_info(self):
        print("开始定位课程")
        write_log("开始定位课程")
        time.sleep(10)
        # 获取课程列表
        try:
            all_class_line = self.driver.find_elements(By.XPATH,f"//div[@class='item-left-course']")
            print(f"共找到{len(all_class_line)}个课程")
            first_class_info=all_class_line[0].text
            first_class_info_list=first_class_info.split('\n')
            print_true(f"课程名:{first_class_info_list[0]} {first_class_info_list[-1]}")
            write_log(f"课程名:#{first_class_info_list[0]}# {first_class_info_list[-1]}")
            all_class_line[0].click()
            time.sleep(10)
            return True
        except:
            print_error("未找到有效课程")
            write_log("**ERROR**未找到有效课程")
            return False


    def watch_video(self,watch_time):
        time.sleep(1)
        try:
            start_tip = self.driver.find_element(By.XPATH, "//i[@class='iconfont iconguanbi']") # 开屏提示
            start_tip.click()
            print("关闭开屏提示")
        except:
            print("未找到开屏提示")
        end_time = time.time()+watch_time
        print_true(f"开始观看视频,时长:{watch_time}s")
        time.sleep(10)
        while end_time >= time.time():
            time.sleep(1)
            #获取当前播放状态的一些信息
            currentTime = self.driver.find_element(By.XPATH, "//span[@class='currentTime']").get_attribute('textContent')#视频当前播放时长
            duration = self.driver.find_element(By.XPATH, "//span[@class='duration']").get_attribute('textContent')#视频总时长
            stop=self.driver.find_element(By.XPATH, "//div[@class='bigPlayButton pointer']")#暂停按钮
            try:#优先弹窗题目处理
                self.driver.find_element(By.XPATH,"//div[@class='el-dialog__wrapper dialog-test']")  # 弹窗主体
                print_error("出现题目弹窗")
                write_log("**WARRING**出现题目弹窗,请注意时间")
                xuanxiang_list = self.driver.find_elements(By.XPATH, "//span[@class='topic-option-item']")  # 选项列表
                for xuanxiang in xuanxiang_list:
                    if xuanxiang.get_attribute('textContent') == 'A.':
                        xuanxiang.click()
                time.sleep(1)
                print('已选择,开始关闭题目')
                webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            except:
                if currentTime == duration:#当前视频播放完成
                    print("当前视频播放完成，即将自动切换下一个视频")
                    write_log("切换视频")
                    video_list=self.driver.find_elements(By.XPATH, "//li[contains(@class,'clearfix video')]")#下一集按钮
                    for i,video in enumerate(video_list):
                        if video.get_attribute('class') == 'clearfix video current_play':
                            if i+1 < len(video_list):#下一集存在
                                video_list[i+1].click()
                                print("完成视频切换")
                                break
                            else:
                                print_error("已到达最后一集，无法切换")
                                print_true("本账号视频已全部播放完成")
                                write_log(f"#{self.username}#所有视频播放完成")
                                return

                elif stop.get_attribute('style') != 'display: none;':#视频暂停时的处理
                    print("当前视频已暂停，即将自动播放")
                    write_log("自动播放视频")
                    start_video=self.driver.find_element(By.XPATH, "//div[@class='videoArea']")#播放的整个显示页面（播放按钮有脚本检测
                    ActionChains(self.driver).click(start_video).perform()


if __name__ == "__main__":
    # 读取用户JSON文件
    with open('users.json', 'r') as file:
        data = json.load(file)
    user_json=data
    while user_json != {}:#直到所有用户都完成
        # 提取和打印键值对
        for username, password in user_json.items():
            zhihuishu = zhihuishu_class()
            # 登录
            try:
                zhihuishu.login(username, password)
            except Exception as e:
                write_log(f'**ERROR**#{username}#登录账号发生错误')
                print_error(f"#{username}#登录账号发生错误")
                print("运行下一账号")
                continue
            # 定位课程
            if zhihuishu.get_class_info():
                print_true("课程定位成功")
            else:
                write_log(f'**ERROR**#{username}#查询课程发生错误')
                print_error(f"#{username}#查询课程发生错误")
                print("运行下一账号")
                continue
            try:
                zhihuishu.watch_video(27*60)
                del user_json[username]#去除完成用户
            except:
                write_log(f'**ERROR**#{username}#观看视频发生错误')
                print_error(f"#{username}#观看视频发生错误")
            print_true(f"#{username}#完成每日刷课！")
            write_log(f'#{username}#完成每日刷课！')


