import requests
from bs4 import BeautifulSoup
import re


def first(url):
    '''
    初始网页: http://www.heibanke.com/lesson/crawler_ex00/
    :return:
    '''
    base_url = 'http://www.heibanke.com/lesson/crawler_ex00/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    result = soup.find('h3').string
    print(result)
    pattern = re.compile(r'\d+')
    number = pattern.search(result).group()
    try:
        url = base_url + number
        first(url)
    except:
        print("正确答案是:" + number)


if __name__ == '__main__':
    first("http://www.heibanke.com/lesson/crawler_ex00/")