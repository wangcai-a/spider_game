import re
import requests
from bs4 import BeautifulSoup
from threading import Thread


login_website = 'http://www.heibanke.com/accounts/login'
pwd_website = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list/'


# 登录记账本
def login_fun():
    s = requests.Session()
    s.get(login_website)     # 访问登录页面获取登录要用的csrftoken
    token1 = s.cookies['csrftoken']      # 保存csrftoken
    # 将csrftoekn存入字段csrfmiddlewaretoken
    dataWebsite1 = {'username': 'user',
                    'password': 'password',
                    'csrfmiddlewaretoken': token1
                    }
    s.post(login_website, data=dataWebsite1)
    return s


class MyThread(Thread):
    def __init__(self, s):
        Thread.__init__(self)
        self.s = s

    def run(self):
        global count
        global pwdlist
        global exit
        ruler = re.compile(r'.*>(\d*)<.*')  # 提取密码位置和值的正则表达式
        while count < 100:
            pwdpage = s.get(pwd_website).content
            password_pos = BeautifulSoup(pwdpage, 'html.parser').findAll('td', {'title': 'password_pos'})
            password_val = BeautifulSoup(pwdpage, 'html.parser').findAll('td', {'title': 'password_val'})
            password_pos_list = []  # 密码位置list
            password_val_list = []  # 密码值list
            if password_pos:
                for i in password_pos:
                    password_pos_list.append(ruler.findall(str(i))[0])
                for j in password_val:
                    password_val_list.append(ruler.findall(str(j))[0])
                print(self.name)
                print(password_pos_list)
                print(password_val_list)
                for index in range(0, len(password_pos_list)):
                    if pwdlist[int(password_pos_list[index]) - 1] == 'x':
                        count += 1
                        pwdlist[int(password_pos_list[index]) - 1] = password_val_list[index]
                print(count)
        if exit == 0:
            exit = 1
            print(''.join(pwdlist))


if __name__ == '__main__':
    s = login_fun()
    exit = 0
    count = 0
    pwdlist = ['x' for i in range(0, 100)]
    for i in range(0, 20):  # 线程数,可自定义
        print("开始第%d个线程" % i)
        thread = MyThread(s)
        thread.start()