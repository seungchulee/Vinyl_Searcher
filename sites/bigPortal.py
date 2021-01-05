bigportalwithQuery = {
    "yes24": "http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=MUSIC&qdomain=CD%2FLP&query=",
    "aladin": "https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Music&SearchWord=",
    "interpark": "http://book.interpark.com/display/displaylist.do?_method=allListCDDVD&sc.shopNo=0000500000&sc.dispNo=001019&query=",
    "naver": "https://search.shopping.naver.com/search/all?query=",
    "Dr.groove": "http://drgroove.co.kr/product/search.html?banner_action=&keyword=",
}
bigportal = {
    "신나라" : "https://www.synnara.co.kr/ss/ss110Main.do",
    "hottracks": "http://www.hottracks.co.kr/ht/biz/record/recordCategoryMain?ctgrId=0003",
    "novvave": "https://novvave.com/shop",
    "seoulrecord": "http://seoulrecord.co.kr/main/index.php",
    "soundwave": "https://sound-wave.co.kr/",
}
bigportalForeign = {
    "vindig": "https://www.vinyl-digital.com/index.php?lang=0&",
    "vinyltarget": "https://www.target.com/s?searchTerm=vinyl&Nao=0",
    "HHV": "https://www.hhv.de/shop/en/vinyl-cd-tape",
}

def printBigPortal(keyword):
    print("----------- ------------- -----------")
    print("with query")
    for key in bigportalwithQuery:
        print(key, bigportalwithQuery[key] + keyword)

    print("----------- ------------- -----------")
    print("without query (just sites)")
    for key in bigportal:
        print(key, bigportal[key])

    print("----------- ------------- -----------")
    print("foreign site (해외 직구 필요)")
    for key in bigportalForeign:
        print(key, bigportalForeign[key])
    print("----------- ------------- -----------")