import requests
import json
from vinyl import Vinyl


def doSeoulVinyl(keyword):
    seoulList = getSeoulVinylResult(keyword)
    print(len(seoulList), "개의 결과가 있습니다")
    for seo in seoulList:
        print(seo.title, seo.price, seo.soldOut, seo.link)


def getSeoulVinylResult(keyword):
    i = 1
    returnList = []
    while True:
        payload = {
            "memberNo": 99047,
            "shopCategoryNoList": "categorized",
            "itemType": "productList",
            "page": i,
            "npp": 16,
            "searchKeyword": keyword,
            "siteNo": 99047
        }
        requestUrl = "https://www.seoulvinyl.com/_shop/getShopProductSummariseBySearchKeyword"
        resp = requests.post(requestUrl, data=payload)
        content = resp.content
        jsonString = json.loads(content)
        products = jsonString['shopProductList']
        if not products:
            break
        for arg in products:
            link = "https://www.seoulvinyl.com/product/" + arg['productAddress']
            title = arg['productName']
            price = arg['productAppliedDiscountEventPrice']
            soldout = productSoldout(arg['productNo'])
            vinyl = Vinyl(link, title, price, soldout, "SeoulVinyl")
            returnList.append(vinyl)
        i += 1
    return returnList


def productSoldout(productNo):
    soldOutRequest = "https://www.seoulvinyl.com/_shop/getShopProductByMemberNoAndProductNo"
    soldPayload = {
        "memberNo": 99047,
        "productNo": productNo,
        "siteNo": 99047,
        "siteLink": "homeboy",
        "pageNo": 0,
    }
    soldResp = requests.post(soldOutRequest, data=soldPayload)
    soldString = json.loads(soldResp.content)
    return soldString['shopProduct']['inventory']['total'] != 0
