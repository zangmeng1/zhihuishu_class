from selenium import webdriver
import requests
import time
import cv2
from selenium.webdriver.common.by import By
import numpy as np
from selenium.webdriver import ActionChains
from selenium import webdriver

def yidun(driver):
    # 获取两张图片
    url_s = driver.find_element(By.XPATH, "//img[@class='yidun_jigsaw']").get_attribute('src')
    url_b = driver.find_element(By.XPATH, "//img[@class='yidun_bg-img']").get_attribute('src')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
    }
    res_s = requests.get(url_s, headers=headers)
    data_s = res_s.content
    res_b = requests.get(url_b, headers=headers)
    data_b = res_b.content
    # 保存图片
    with open('pic_s.png', 'wb') as f:
        f.write(data_s)
    with open('pic_b.png', 'wb') as f:
        f.write(data_b)

    # 使用opencv读取两张图片
    simg = cv2.imread('pic_s.png')
    bimg = cv2.imread('pic_b.png')

    # 识别图片边缘
    bg_edge = cv2.Canny(bimg, 100, 200)
    tp_edge = cv2.Canny(simg, 100, 200)

    # 灰度处理，降低偏差
    s_img = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    b_img = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)

    # 保存两张描边处理的图片
    cv2.imwrite('hui_simg.png', s_img)
    cv2.imwrite('hui_bimg.png', b_img)

    # opencv的匹配算法，匹配模块寻找两张图片的相似之处
    res = cv2.matchTemplate(b_img, s_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
    # 绘制方框
    th, tw = s_img.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(b_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite("out.png", b_img)  # 保存在本地
    x = tl[0]+10#制作偏移（？
    #print('x:',x)
    # 定位到滑块
    ele = driver.find_element(By.XPATH,"//div[contains(@class,'yidun_slider')]")
    # 实例化对象
    action = ActionChains(driver)
    # 拖动滑块
    time.sleep(1)
    action.drag_and_drop_by_offset(ele, xoffset=x, yoffset=0).perform()
    time.sleep(1)
    # 定位到验证成功
    time.sleep(1)
