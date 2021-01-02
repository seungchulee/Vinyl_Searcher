class Vinyl:
    # soldOut : false == 품절, true == 재고 있음
    def __init__(self, link, title, price, soldOut, where, img_src):
        self.link = link
        self.title = title
        self.price = price
        self.soldOut = soldOut
        self.where = where
        self.img_src = img_src
