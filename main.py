from gimbab import getGimbabSearchResult

if __name__ == "__main__":
    keyword = input()
    gimbabList = getGimbabSearchResult(keyword)
    for gim in gimbabList:
        print(gim.price, gim.title, gim.link, gim.soldOut)


