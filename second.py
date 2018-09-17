import requests
from bs4 import BeautifulSoup


def second():
    login_url = 'http://www.heibanke.com/lesson/crawler_ex01/'
    data = {
        "password": 1,
        "username": "peng1",
        "csrf": "pLtxoOjIFZG4XbVn2t1JvnpN1Y8SGSGJ"
    }
    for n in range(1, 31):
        data["password"] = n
        res = requests.post(login_url, data=data)
        soup = BeautifulSoup(res.text, 'lxml')
        result = soup.find('h3').string
        print(result)
        if result != "您输入的密码错误, 请重新输入":
            print("正确密码是:" + str(n))
            break


if __name__ == '__main__':
    second()