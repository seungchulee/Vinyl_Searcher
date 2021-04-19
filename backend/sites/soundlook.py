from bs4 import BeautifulSoup
from back.bypass import returnContent
from back.vinyl import Vinyl


def doSoundLook(keyword):
    sLookList = getSoundLookResult(keyword)
    print(len(sLookList), "개의 결과가 있습니다")
    for slo in sLookList:
        print(slo.title, slo.price, slo.soldOut, slo.link)


def getSoundLookResult(keyword):
    returnList = []
    page = 1
    while True:
        url = "http://soundlook.co.kr/product/search.html?banner_action=&keyword=" + keyword + "&page=" + str(page)
        content = returnContent(url)
        bs = BeautifulSoup(content, 'html.parser')
        if not bs.find_all('ul', attrs={'class':'prdList'}):
            break
        pageInfo = bs.find_all('li', class_=["item_list", "xans-record-"])
        for vin in pageInfo:
            title = vin.find('strong', attrs={'class':'name'})
            if title is None:
                continue
            soldout = True
            if vin.find('img', attrs={'alt': "품절"}):
                soldout = False
            price = vin.find('li', attrs={'class': 'price'}).text
            link = "http://soundlook.co.kr" + vin.find('a')['href']
            img_src = "http://" + vin.find('img')['src'][2:]
            if soldout:
                vinyl = Vinyl(link, title.text, price, soldout, "사운드룩", img_src)
                returnList.append(vinyl)
        page += 1

    return returnList

