import requests
from bs4 import BeautifulSoup
from threading import Thread


def login():
    login_url = "http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex03/"

    # 获取token
    session = requests.session()
    session.get(login_url)
    csrf = session.cookies['csrftoken']

    # 构造header,data并登录
    headers = {"User_Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, "
                             "like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
    data1 = {
        "csrfmiddlewaretoken": csrf,
        "username": "peng1",
        "password": "123456"
    }
    session.post(login_url, data=data1, headers=headers)
    return session


# 创建线程
class MyThread(Thread):
    def __init__(self, session):
        Thread.__init__(self)
        self.session = session

    def run(self):
        global result_password
        global count
        # 进入闯关页面,开始闯关
        while count < 100:
            # 因为密码是随机给出的,所以只要不断的爬取第一页就好了
            password_url = "http://www.heibanke.com/lesson/crawler_ex03/pw_list/"
            res = session.get(password_url)
            soup = BeautifulSoup(res.text, 'lxml')
            positions = soup.find_all('td', title="password_pos")
            passwords = soup.find_all('td', title="password_val")
            n = 0
            while n < len(positions):
                result_password.update({positions[n].text: passwords[n].text})
                n += 1
            count = len(result_password.keys())
            print(self.name)
            print("已获取密码位数%d" % count)
        if count > 99:
            n = 1
            password = ''
            while n < 101:
                password = password + result_password[str(n)]
                n += 1
            print(password)


if __name__ == '__main__':
    session = login()
    result_password = dict()
    count = 0
    for n in range(1, 20):
        print("线程%d启动" % n)
        thread = MyThread(session)
        thread.start()