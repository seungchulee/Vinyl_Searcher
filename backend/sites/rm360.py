from pprint import pprint

from back.bypass import returnContent
from bs4 import BeautifulSoup
from back.vinyl import Vinyl

def dorm360(keyword):
    rmList = dorm360List(keyword)
    print(len(rmList), "개의 결과가 있습니다")
    for rm in rmList:
        print(rm.title, rm.price, rm.soldOut, rm.link)


def dorm360List(keyword):
    returnList = []
    page = 1
    while True:
        url = "http://rm360.cafe24.com/product/search.html?banner_action=&keyword=" + keyword + "&page=" + str(page)
        content = returnContent(url)
        bb = BeautifulSoup(content, 'html.parser')
        bs = bb.find_all('li', attrs={'class': 'xans-record-'})
        bp = False
        pageInfo = []
        for arg in bs:
            if arg.find('div', attrs={'class':'thumbnail'}) is not None:
                bp = True
                pageInfo.append(arg)
        if not bp:
            break
        for vin in pageInfo:
            title = vin.find('p', attrs={'class': 'name'})
            price = vin.find('p', attrs={'class': 'price'}).text[4:]
            link = "http://rm360.cafe24.com/" + title.find('a')['href']
            soldout = False
            if vin.find('p', attrs={'class':'icon'}).find('img') is None:
                soldout = True
            img_src = "http://" + vin.find('div', attrs={'class': 'thumbnail'}).find('img')['src'][4:]
            if soldout:
                vinyl = Vinyl(link, title.text, price, soldout, "rm360", img_src)
                returnList.append(vinyl)
        page += 1

    return returnList

