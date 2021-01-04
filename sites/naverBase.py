from bs4 import BeautifulSoup
import requests
from back.vinyl import Vinyl

naverBase = {
    "아이텐": "https://smartstore.naver.com/i-10",
    "기기레코즈": "https://smartstore.naver.com/gigirecords",
    "바이닐코리아": "https://smartstore.naver.com/waxtime",
    "마이페이보릿스토어": "https://smartstore.naver.com/cinemastore",
    "하이닐": "https://smartstore.naver.com/hinyl",
    "테리픽잼": "https://smartstore.naver.com/terrific_jam",
    "레코드스톡": "https://smartstore.naver.com/recordstock",
    "라보앤드": "https://smartstore.naver.com/lavoand/",
    "마뮤": "https://smartstore.naver.com/mamustore",
    "판다바이닐": "https://smartstore.naver.com/pandavinyl",
    "뮤직랜드": "https://smartstore.naver.com/musicland"
}


def doNaver(keyword):
    for site in naverBase:
        naverList = getNaverBaseResult(keyword, site)
        print("----------- ------------- -----------")
        print(site, "에서", len(naverList), "개의 결과가 있습니다")
        for nav in naverList:
            print(nav.title, nav.price, nav.soldOut, nav.link)


def getPageType(url):
    resp = requests.get(url)
    bs = BeautifulSoup(resp.content, 'html.parser')
    type = ""
    if bs.find_all('div', attrs={'class': "theme_basic"}):
        type = "basic"
    elif bs.find_all('div', attrs={'class': "theme_trendy"}):
        type = "trendy"

    return len(bs.find_all('a', attrs={'class': 'UWN4IvaQza'})), type


def getNaverBaseResult(keyword, site):
    returnList = []
    url = naverBase[site] + "/search?q=" + keyword
    page, type = getPageType(url)
    if type == "":
        return returnList
    for i in range(1, page+1):
        requestUrl = url + "&page=" + str(i)
        resp = requests.get(requestUrl)
        bs = BeautifulSoup(resp.content, 'html.parser')
        if type == "basic":
            vinyls = bs.find_all('li', attrs={'class': '_3Lde95QPKh'})
            for vin in vinyls:
                title = vin.find('strong', attrs={'class': '_3W4A_RFJRS'}).text
                price = vin.find('span', attrs={'class':'_11N87Svo1h'}).text
                link = "https://smartstore.naver.com" + vin.find('a', attrs={'class':'cj7gkLIEbC N=a:lst.product linkAnchor'})['href']
                img_src = vin.find('img', attrs={'class':'_25CKxIKjAk'})['src']
                soldout = False
                if vin.find('span', attrs={'class': 'text blind'}) is None:
                    soldout = True
                if soldout:
                    vinyl = Vinyl(link, title, price, soldout, site, img_src)
                    returnList.append(vinyl)
        elif type == "trendy":
            vinyls = bs.find_all('li', attrs={'class': '_3S7Ho5J2Ql'})
            for vin in vinyls:
                title = vin.find('strong', attrs={'class': '_1Zvjahn0GA'}).text
                price = vin.find('span', attrs={'class': '_3_9J443eIx'}).text
                link = "https://smartstore.naver.com" + vin.find('a', attrs={'class':'_1vVKEk_wsi N=a:lst.product linkAnchor'})['href']
                img_src = vin.find('img', attrs={'class':'_25CKxIKjAk'})['src']
                soldout = False
                if vin.find('span', attrs={'class': 'text blind'}) is None:
                    soldout = True
                if soldout:
                    vinyl = Vinyl(link, title, price, soldout, site, img_src)
                    returnList.append(vinyl)
    return returnList
