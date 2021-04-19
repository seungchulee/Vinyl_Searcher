import time
import requests
import json
from back.vinyl import Vinyl
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def doWelcomeRecords(keyword):
    welcomeResult = getWelcomeResult(keyword)
    print(len(welcomeResult), "개의 결과가 있습니다")
    for wel in welcomeResult:
        print(wel.title, wel.price, wel.soldOut, wel.link)


def getWelcomeResult(keyword):
    i = 1
    returnList = []
    while True:
        payload = {
            "memberNo": 103345,
            "shopCategoryNoList": "categorized",
            "itemType": "productList",
            "page": i,
            "npp": 48,
            "searchKeyword": keyword,
            "siteNo": 103345,
            "siteLink": "welcomerecords"
        }
        requestUrl = "https://welcomerecords.kr/_shop/getShopProductSummariseBySearchKeyword"
        try:
            resp = requests.post(requestUrl, data=payload)
        except requests.exceptions.ConnectionError as e:
            print("WELCOME RECORDS ERROR!!")
            welcomeUrl = "https://welcomerecords.kr/productSearch?productSearchKeyword=" + keyword
            print("try visit here ---->", welcomeUrl)
            break

        content = resp.content
        jsonString = json.loads(content)
        products = jsonString['shopProductList']
        if not products:
            break
        for arg in products:
            link = "https://www.welcomerecords.kr/product/" + arg['productAddress']
            title = arg['productName']
            price = arg['productAppliedDiscountEventPrice']
            img_src = arg['imageUrl']
            soldout = productSoldout(arg['productAddress'])
            if soldout:
                vinyl = Vinyl(link, title, price, soldout, "WelcomeRecords", img_src)
                returnList.append(vinyl)
        i += 1
    return returnList


def productSoldout(name):
    resp = requests.get("https://www.welcomerecords.kr/product/" + name)
    bs = BeautifulSoup(resp.content, 'html.parser')
    b = bs.find('button', attrs={'class': 'buyNow designSettingElement button notWorkingButton'})
    return b is None


def productPrevSoldout(productNo):
    soldOutRequest = "https://www.welcomerecords.kr/_shop/getShopProductByMemberNoAndProductNo"
    soldPayload = {
        "memberNo": 103345,
        "productNo": productNo,
        "siteNo": 103345,
        "siteLink": "welcomerecords",
        "pageNo": 0,
    }
    soldResp = requests.post(soldOutRequest, data=soldPayload)
    soldString = json.loads(soldResp.content)
    return soldString['shopProduct']['sellStatus'] != "soldOut_selling"
