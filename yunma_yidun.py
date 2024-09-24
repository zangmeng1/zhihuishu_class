import base64
import configparser
import requests


config = configparser.ConfigParser()
config.read('config.ini', encoding='UTF-8')
yunma_token=token = config.get('system', 'yunma_token')

def yunma_kongjian(img_url,extra):
    global yunma_token

    # 保存图片
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
    }
    res_s = requests.get(img_url, headers=headers)
    data_s = res_s.content
    with open('yidun_kongjian.png', 'wb') as f:
        f.write(data_s)

    with open('yidun_kongjian.png', 'rb') as f:
        b = base64.b64encode(f.read()).decode()
    url = "http://api.jfbym.com/api/YmServer/customApi"
    data = {
        "token":yunma_token,
        "type": "30109",
        "image": b,
        "extra": extra
    }
    _headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=_headers, json=data).json()
    print(response)
    if response['code'] == 10000:
        print("云码-空间推理验证码识别 成功")
        xyoffset = response['data']['data'].split(',')
        return xyoffset
    else:
        print("云码-空间推理验证码识别 失败")
        xyoffset=[88,88]
        return xyoffset


if __name__ == '__main__':
    #请求示例
    yunma_kongjian("https://necaptcha.nosdn.127.net/ea79265e582a4056aff10b7de369f32a.jpg","请点击红色小写p朝向一样的大写V")