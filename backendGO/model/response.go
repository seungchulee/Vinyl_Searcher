package model

type RespUnit struct {
	Name    string `json:"name"`
	Price   int    `json:"salePrice"`
	ImgSrc  string `json:"representativeImageUrl"`
	SoldOut string `json:"productStatusType"`
	Id      int    `json:"id"`
}
