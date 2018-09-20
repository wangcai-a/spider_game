import requests
from bs4 import BeautifulSoup


def third():
    login_url = "http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex02/"

    # 获取csrftoken
    session = requests.session()
    res = session.get(login_url)
    csrf = res.cookies['csrftoken']

    # 构造header,data并登录
    headers = {"User_Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, "
                             "like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
    data1 = {
        "csrfmiddlewaretoken": csrf,
        "username": "peng1",
        "password": "123456"
    }
    res = session.post(login_url, data=data1, headers=headers)
    # 进入闯关页面,开始闯关
    url = "http://www.heibanke.com/lesson/crawler_ex02/"

    data2 = {
        "password": 1,
        "username": "peng1",
        "csrfmiddlewaretoken": ""
    }

    for n in range(1, 31):
        res = session.get(url)
        data2["password"] = n
        data2["csrfmiddlewaretoken"] = res.cookies["csrftoken"]
        res = session.post(url, data=data2)
        soup = BeautifulSoup(res.text, 'lxml')
        result = soup.find('h3').string
        print(result)
        if result != "您输入的密码错误, 请重新输入":
            print("正确密码是:" + str(n))
            break


if __name__ == '__main__':
    third()