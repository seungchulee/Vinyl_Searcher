import requests
import json
from back.vinyl import Vinyl
from bs4 import BeautifulSoup

def doSoundsGood(keyword):
    soundsList = getSoundsGoodResult(keyword)
    print(len(soundsList), "개의 결과가 있습니다")
    for sgo in soundsList:
        print(sgo.title, sgo.price, sgo.soldOut, sgo.link)


def getSoundsGoodResult(keyword):
    i = 1
    returnList = []
    while True:
        payload = {
            "memberNo": 27989,
            "shopCategoryNoList": "categorized",
            "itemType": "productList",
            "page": i,
            "npp": 100,
            "searchKeyword": keyword,
            "siteNo": 27989
        }
        requestUrl = "https://soundsgood-store.com/_shop/getShopProductSummariseBySearchKeyword"
        resp = requests.post(requestUrl, data=payload)
        content = resp.content
        jsonString = json.loads(content)
        products = jsonString['shopProductList']
        if not products:
            break
        for arg in products:
            link = "https://www.soundsgood-store.com/product/" + arg['productAddress']
            title = arg['productName']
            price = arg['productAppliedDiscountEventPrice']
            img_src = arg['imageUrl']
            prevsoldout = productPrevSoldout(arg['productNo'])
            if prevsoldout:
                soldout = productSoldout(arg['productAddress'])
                if soldout:
                    vinyl = Vinyl(link, title, price, soldout, "SoundsGood", img_src)
                    returnList.append(vinyl)
        i += 1
    return returnList


def productSoldout(name):
    resp = requests.get("https://www.soundsgood-store.com/product/" + name)
    bs = BeautifulSoup(resp.content, 'html.parser')
    b = bs.find('div', attrs={'class': 'productQuantityDiv row designSettingElement text-body'})
    return b is not None


def productPrevSoldout(productNo):
    soldOutRequest = "https://www.soundsgood-store.com/_shop/getShopProductByMemberNoAndProductNo"
    soldPayload = {
        "memberNo": 27989,
        "productNo": productNo,
        "siteNo": 27989,
        "siteLink": "soundsgood_store",
        "pageNo": 0,
    }
    soldResp = requests.post(soldOutRequest, data=soldPayload)
    soldString = json.loads(soldResp.content)
    return soldString['shopProduct']['sellStatus'] != "soldOut_selling"
