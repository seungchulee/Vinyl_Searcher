from bs4 import BeautifulSoup
import requests
from back.vinyl import Vinyl
import json

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
    "뮤직랜드": "https://smartstore.naver.com/musicland",
    "구해줘굿즈": "https://smartstore.naver.com/getgoods",
    "아메리칸오리진": "https://smartstore.naver.com/watsons",
    "모카홀릭": "https://smartstore.naver.com/byeolne",
    "쳇베이커리": "https://smartstore.naver.com/chetbakery",
    "바이어티": "https://smartstore.naver.com/buyerty",
    "라운드뮤직": "https://smartstore.naver.com/sun_musicstore2019",
}

naverCode = {
    "아이텐": "https://smartstore.naver.com/i/v1/stores/500270672/categories/ad7d0d900c8d43b0b53977186cfa12bc/products?categoryId=ad7d0d900c8d43b0b53977186cfa12bc&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
    "기기레코즈": "100632872",
    "바이닐코리아": "100599518",
    "마이페이보릿스토어": "100517823",
    "하이닐": "100797246",
    "테리픽잼": "100710783",
    "레코드스톡": "100804461",
    "라보앤드": "100078012",
    "마뮤": "100787591",
    "판다바이닐": "https://smartstore.naver.com/i/v1/stores/100975984/categories/ALL/products?categoryId=ALL&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
    "뮤직랜드": "500015866",
    "구해줘굿즈": "https://smartstore.naver.com/i/v1/stores/100610551/categories/77f0e03857bf4726b9ead59820937e99/products?categoryId=77f0e03857bf4726b9ead59820937e99&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
    "아메리칸오리진": "https://smartstore.naver.com/i/v1/stores/100560456/categories/50000058/products?categoryId=50000058&categorySearchType=STDCATG&sortType=RECENT&free=false&page=1&pageSize=40",
    "모카홀릭": "https://smartstore.naver.com/i/v1/stores/100523535/categories/a04cee97cd7e47328295c39c96fcc1f1/products?categoryId=a04cee97cd7e47328295c39c96fcc1f1&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
    "쳇베이커리": "100580090",
    "바이어티": "100646105",
    "라운드뮤직": "https://smartstore.naver.com/i/v1/stores/100747626/categories/ALL/products?categoryId=ALL&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
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
                pr = vin.find('span', attrs={'class': '_11N87Svo1h'})
                if pr is None:
                    continue
                price = pr.text
                link = "https://smartstore.naver.com" + vin.find('a', attrs={'class':'cj7gkLIEbC N=a:lst.product linkAnchor'})['href']
                img_src = vin.find('img', attrs={'class':'_25CKxIKjAk'})['src']
                soldout = True
                soldoutText = vin.find_all('span', attrs={'class': 'text blind'})
                for st in soldoutText:
                    if "일시 품절" in str(st):
                        soldout = False
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
                soldout = True
                soldoutText = vin.find_all('span', attrs={'class': 'text blind'})
                for st in soldoutText:
                    if "일시 품절" in str(st):
                        soldout = False
                if soldout:
                    vinyl = Vinyl(link, title, price, soldout, site, img_src)
                    returnList.append(vinyl)
    return returnList


def returnVinyl(products, site, newLink):
    return_list = []
    save_str = ""
    fileUrl = "./back/" + site + ".txt"
    try:
        fileData = open(fileUrl, "r")
        existed_str = fileData.readline()
        fileData.close()
    except FileNotFoundError:
        fileData = open(fileUrl, "w")
        existed_str = ""
        fileData.close()

    for prd in products:
        if len(return_list) == 10:
            break
        if not newLink:
            prd = prd['simpleProduct']
        title = prd['name']
        price = prd['salePrice']
        soldout = True
        if prd['productStatusType'] == "OUTOFSTOCK":
            soldout = False
        link = naverBase[site] + "/products/" + str(prd['id'])
        img_src = prd['representativeImageUrl']
        if soldout:
            vinyl = Vinyl(link, title, price, soldout, link, img_src)
            save_str += str(prd['id'])
            return_list.append(vinyl)

    f = open(fileUrl, 'w')
    f.write(save_str)
    f.close()
    if existed_str != save_str:
        return return_list, False
    else:
        return return_list, True


def getNewNaver(site):
    code = naverCode[site]
    if "http" in code:
        url = code
    else:
        url = "https://smartstore.naver.com/i/v1/stores/" + code + "/pc-widgets/whole-products?sort=RECENT"
    resp = requests.get(url)
    data = json.loads(resp.content)

    if "http" in code:
        products = data['simpleProducts']
        return returnVinyl(products, site, True)
    else:
        return returnVinyl(data, site, False)



def showNewNaver():
    for site in naverBase:
        naverList, same = getNewNaver(site)
        print("----------- ------------- -----------")
        print(site, "에서", len(naverList), "개의 결과가 있습니다")
        if not same:
            print("SOMETHING CHANGED!!!")
        for nav in naverList:
            print(nav.title, nav.price, nav.soldOut, nav.link)