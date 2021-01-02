from bs4 import BeautifulSoup
from bypass import returnContent
from vinyl import Vinyl

def doBeatitMusic(keyword):
    seoulList = getBeatitMusicResult(keyword)
    print(len(seoulList), "개의 결과가 있습니다")
    for seo in seoulList:
        print(seo.title, seo.price, seo.soldOut, seo.link)

def getBeatitMusicResult(keyword):
    returnList = []
    pagenation = getPagenation(keyword)
    if pagenation == -1:
        return returnList
    for i in range(1, pagenation + 1):
        url = "http://beatit.co.kr/product/search.html?banner_action=&keyword=" + keyword + "&page=" + str(i)
        content = returnContent(url)
        bs = BeautifulSoup(content, 'html.parser')
        pageInfo = bs.find_all('li', attrs={'class':"xans-record-"})
        for data in pageInfo:
            # if "anchorBox" in data:
            title = data.find('strong', attrs={'class':'name'})
            if title is not None:
                if data.find('img', attrs={'class':'icon_img'}):
                    soldout = False
                else:
                    soldout = True
                vinylTitle = title.text.split(':')[-1].strip()
                link = "http://beatit.co.kr" + title.find('a')['href']
                priceTag = data.find('ul', attrs={'class':'xans-element- xans-search xans-search-listitem spec'})
                price = priceTag.find_all('span', attrs={'style':'font-size:12px;color:#008BCC;font-weight:bold;'})[-1].text
                img_src = "http://" + data.find('img')['src'][2:]
                vinyl = Vinyl(link, vinylTitle, price, soldout, "beatit", img_src)
                returnList.append(vinyl)

    return returnList


def getPagenation(keyword):
    url = "http://beatit.co.kr/product/search.html?banner_action=&keyword=" + keyword
    content = returnContent(url)
    bs = BeautifulSoup(content, 'html.parser')
    pageInfo = bs.find("a", attrs={'class': 'last'})
    if pageInfo is None:
        return -1
    page = pageInfo['href'].split("=")[-1]
    if page == "#none":
        return 1
    else:
        return int(page)
