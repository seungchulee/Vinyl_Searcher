from bs4 import BeautifulSoup
from back.bypass import returnContent
from back.vinyl import Vinyl


def doGimBab(keyword):
    gimbabList = getGimbabSearchResult(keyword)
    print(len(gimbabList), "개의 결과가 있습니다")
    for gim in gimbabList:
        print(gim.title, gim.price, gim.soldOut, gim.link)


def doGimBab2(keyword):
    gimbabList = getGimbab2SearchResult(keyword)
    print(len(gimbabList), "개의 결과가 있습니다")
    for gim in gimbabList:
        print(gim.title, gim.price, gim.soldOut, gim.link)


def getGimbabSearchResult(keyword):
    pagination = getPagination(keyword)
    if pagination == -1:
        return []
    returnList = []
    for idx in range(pagination):
        url = "http://gimbabrecords.com/product/search.html?banner_action=&keyword=" + keyword + "&page=" + str(idx+1)
        content = returnContent(url)
        bs = BeautifulSoup(content, 'html.parser')
        li_element = bs.find_all("li", attrs={'class': 'item xans-record-'})

        for el in li_element:
            img_src = "http://" + el.find('img')['src'][2:]
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
            if soldout:
                vinylClass = Vinyl(link, title, price, soldout, "김밥레코즈", img_src)
                returnList.append(vinylClass)
    return returnList


def getPagination(keyword):
    url = "http://gimbabrecords.com/product/search.html?banner_action=&keyword=" + keyword
    content = returnContent(url)
    bs = BeautifulSoup(content, 'html.parser')
    paging = bs.find_all("div", attrs={'id': 'paging'})
    if not paging:
        return -1
    else:
        paging = paging[0]
    pagination = paging.find_all("li", attrs={'class':'xans-record-'})
    return len(pagination)


def getPagination2(content):
    bs = BeautifulSoup(content, 'html.parser')
    page = bs.find('a', attrs={'class':'last'})
    if page is None:
        return -1
    page = page['href']
    if page == "#none":
        return 1
    else:
        idx = page.find("page")
        return int(page[idx+5:])


def getGimbab2SearchResult(keyword):
    returnList = []
    url = "http://gimbabrecords2.com/product/search.html?banner_action=&keyword=" + keyword
    content = returnContent(url)
    page = getPagination2(content)
    if page == -1:
        return returnList
    for i in range(1, page+1):
        url = "http://gimbabrecords2.com/product/search.html?banner_action=&keyword=" + keyword + "&page=" + str(i)
        content = returnContent(url)
        bb = BeautifulSoup(content, 'html.parser')
        bs = bb.find_all("li", attrs={'class': 'xans-record-'})
        bp = False
        pageInfo = []
        for arg in bs:
            if arg.find('div', attrs={'class':'thumbnail'}) is not None:
                bp = True
                pageInfo.append(arg)
        if not bp:
            break
        for vin in pageInfo:
            title = vin.find('span', attrs={'class': 'name'})
            price = vin.find('span', attrs={'class': 'price'}).text
            link = "http://gimbabrecords2.com/" + title.find('a')['href']
            soldout = False
            if vin.find('div', attrs={'class': 'promotion'}).find('img', attrs={'alt':'품절'}) is None:
                soldout = True
            img_src = "http://" + vin.find('div', attrs={'class': 'thumbnail'}).find('img')['src'][2:]
            if soldout:
                vinyl = Vinyl(link, title.text, price, soldout, "김밥레코즈2", img_src)
                returnList.append(vinyl)
    return returnList

