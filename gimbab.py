import requests
from bs4 import BeautifulSoup
from bypass import returnContent
from vinyl import Vinyl

def getGimbabSearchResult(keyword):
    pagination = getPagination(keyword)
    returnList = []
    for idx in range(pagination):
        url = "http://gimbabrecords.com/product/search.html?banner_action=&keyword=" + keyword + "&page=" + str(idx+1)
        content = returnContent(url)
        bs = BeautifulSoup(content, 'html.parser')
        li_element = bs.find_all("li", attrs={'class': 'item xans-record-'})

        for el in li_element:
            spanData = el.find_all("span", attrs={'style':"font-size:13px;color:#000000;font-weight:bold;"})
            isSoldOut = el.find_all("img", attrs={'alt': "품절"})
            href = el.find("a")['href']
            link = "http://gimbabrecords.com" + href
            soldout = False
            title = ""
            price = ""
            if not isSoldOut:
                soldout = True
            if len(spanData) != 4:
                continue
            for i in range(len(spanData)):
                if i == 1:
                    title = spanData[i].text
                if i == 3:
                    price = spanData[i].text
            vinylClass = Vinyl(link, title, price, soldout)
            returnList.append(vinylClass)
    return returnList

def getPagination(keyword):
    url = "http://gimbabrecords.com/product/search.html?banner_action=&keyword=" + keyword
    content = returnContent(url)
    bs = BeautifulSoup(content, 'html.parser')
    paging = bs.find_all("div", attrs={'id': 'paging'})[0]
    pagination = paging.find_all("li", attrs={'class':'xans-record-'})
    return len(pagination)