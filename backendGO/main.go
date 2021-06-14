package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"
	"strings"
	_ "strings"

	"github.com/gorilla/mux"
)

var naverBase = map[string]string{
	"아이텐":       "https://smartstore.naver.com/i-10",
	"기기레코즈":     "https://smartstore.naver.com/gigirecords",
	"바이닐코리아":    "https://smartstore.naver.com/vinylkor",
	"마이페이보릿스토어": "https://smartstore.naver.com/cinemastore",
	"하이닐":       "https://smartstore.naver.com/hinyl",
	"테리픽잼":      "https://smartstore.naver.com/terrific_jam",
	"레코드스톡":     "https://smartstore.naver.com/recordstock",
	"라보앤드":      "https://smartstore.naver.com/lavoand",
	"마뮤":        "https://smartstore.naver.com/mamustore",
	"판다바이닐":     "https://smartstore.naver.com/pandavinyl",
	"뮤직랜드":      "https://smartstore.naver.com/musicland",
	"구해줘굿즈":     "https://smartstore.naver.com/getgoods",
	"아메리칸오리진":   "https://smartstore.naver.com/watsons",
	"모카홀릭":      "https://smartstore.naver.com/byeolne",
	"쳇베이커리":     "https://smartstore.naver.com/chetbakery",
	"바이어티":      "https://smartstore.naver.com/buyerty",
	"라운드뮤직":     "https://smartstore.naver.com/sun_musicstore2019",
	"인펙션스 레코드":  "https://smartstore.naver.com/infectionsrecord",
	"비트볼 뮤직":    "https://smartstore.naver.com/beatball",
	"서울 바이닐":    "https://smartstore.naver.com/seoulvinyl",
	"더 슬로우 샵":   "https://smartstore.naver.com/theslowshop",
	"서울 레코드":    "https://smartstore.naver.com/seoulrecord",
	"사운드룩":      "https://smartstore.naver.com/soundlook",
	"드림 레코드":    "https://smartstore.naver.com/dreamrec",
	"바이닐 앤 바이브": "https://smartstore.naver.com/vinylnvibe",
	"아이러브뮤직":    "https://smartstore.naver.com/ilovemusic_kr",
	"슬로우바이닐":    "https://smartstore.naver.com/slowvinyl",
}

var code = map[string]string{
	"아이텐":       "https://smartstore.naver.com/i/v1/stores/500270672/categories/ad7d0d900c8d43b0b53977186cfa12bc/products?categoryId=ad7d0d900c8d43b0b53977186cfa12bc&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"기기레코즈":     "https://smartstore.naver.com/i/v1/stores/100632872/categories/ALL/products?categoryId=ALL&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"바이닐코리아":    "https://smartstore.naver.com/i/v1/stores/100599518/categories/ALL/products?categoryId=ALL&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"마이페이보릿스토어": "100517823",
	"하이닐":       "100797246",
	"테리픽잼":      "https://smartstore.naver.com/i/v1/stores/100710783/categories/ALL/products?categoryId=ALL&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"레코드스톡":     "100804461",
	"라보앤드":      "https://smartstore.naver.com/i/v1/stores/100078012/categories/50000058/products?categoryId=50000058&categorySearchType=STDCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"마뮤":        "100787591",
	"판다바이닐":     "https://smartstore.naver.com/i/v1/stores/100975984/categories/ALL/products?categoryId=ALL&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"뮤직랜드":      "500015866",
	"구해줘굿즈":     "https://smartstore.naver.com/i/v1/stores/100610551/categories/77f0e03857bf4726b9ead59820937e99/products?categoryId=77f0e03857bf4726b9ead59820937e99&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"아메리칸오리진":   "https://smartstore.naver.com/i/v1/stores/100560456/categories/50000058/products?categoryId=50000058&categorySearchType=STDCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"모카홀릭":      "https://smartstore.naver.com/i/v1/stores/100523535/categories/a04cee97cd7e47328295c39c96fcc1f1/products?categoryId=a04cee97cd7e47328295c39c96fcc1f1&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"쳇베이커리":     "100580090",
	"바이어티":      "https://smartstore.naver.com/i/v1/stores/100646105/categories/ALL/products?categoryId=ALL&categorySearchType=STDCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"라운드뮤직":     "https://smartstore.naver.com/i/v1/stores/100747626/categories/ALL/products?categoryId=ALL&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"인펙션스 레코드":  "https://smartstore.naver.com/i/v1/stores/100619159/categories/ALL/products?categoryId=ALL&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"비트볼 뮤직":    "https://smartstore.naver.com/i/v1/stores/500280301/categories/ALL/products?categoryId=ALL&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"서울 바이닐":    "https://smartstore.naver.com/i/v1/stores/100129192/categories/ALL/products?categoryId=ALL&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"더 슬로우 샵":   "https://smartstore.naver.com/i/v1/stores/101009441/categories/ALL/products?categoryId=ALL&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"서울 레코드":    "500173380",
	"사운드룩":      "https://smartstore.naver.com/i/v1/stores/500017851/categories/e77769162d0441328d8fd5b8bd05aa97/products?categoryId=e77769162d0441328d8fd5b8bd05aa97&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"드림 레코드":    "100116811",
	"바이닐 앤 바이브": "101150414",
	"아이러브뮤직":    "https://smartstore.naver.com/i/v1/stores/100239915/categories/bfec08c6c034482bbabdabad2f026784/products?categoryId=bfec08c6c034482bbabdabad2f026784&categorySearchType=DISPCATG&sortType=RECENT&free=false&page=1&pageSize=40",
	"슬로우바이닐":    "100795359",
}

type newData struct {
	SimpleProduct []dataUnit `json:"simpleProducts"`
}

type oldData struct {
	SimpleProduct dataUnit `json:"simpleProduct"`
}

type dataUnit struct {
	Name    string `json:"name"`
	Price   int    `json:"salePrice"`
	ImgSrc  string `json:"representativeImageUrl"`
	SoldOut string `json:"productStatusType"`
	Id      int    `json:"id"`
}

type returnDataFormat struct {
	Name   string
	Price  int
	ImgSrc string
	Link   string
	Where  string
	Id     int
}

func getNewNaver(code, url, where string, newChan chan []returnDataFormat) {
	var returns []returnDataFormat
	requestUrl := ""
	isNew := false
	if strings.Contains(code, "http") {
		requestUrl = code
		isNew = true
	} else {
		requestUrl = "https://smartstore.naver.com/i/v1/stores/" + code + "/pc-widgets/whole-products?sort=RECENT"
	}
	resp, err := http.Get(requestUrl)
	if err != nil {
		panic(err)
	}
	if isNew {
		respBody, _ := ioutil.ReadAll(resp.Body)
		var respData newData
		err = json.Unmarshal(respBody, &respData)
		if err != nil {
			panic(err)
		}
		for _, data := range respData.SimpleProduct {
			if data.SoldOut == "OUTOFSTOCK" {
				continue
			}
			returns = append(returns, returnDataFormat{
				Id:     data.Id,
				Name:   data.Name,
				ImgSrc: data.ImgSrc,
				Price:  data.Price,
				Where:  where,
				Link:   url + "/products/" + strconv.Itoa(data.Id),
			})
		}
	} else {
		respBody, _ := ioutil.ReadAll(resp.Body)
		var respData []oldData
		err = json.Unmarshal(respBody, &respData)
		if err != nil {
			panic(err)
		}
		for _, data := range respData {
			if data.SimpleProduct.SoldOut == "OUTOFSTOCK" {
				continue
			}
			returns = append(returns, returnDataFormat{
				Id:     data.SimpleProduct.Id,
				Name:   data.SimpleProduct.Name,
				ImgSrc: data.SimpleProduct.ImgSrc,
				Price:  data.SimpleProduct.Price,
				Where:  where,
				Link:   url + "/products/" + strconv.Itoa(data.SimpleProduct.Id),
			})
		}
	}
	newChan <- returns
}

func makeNewResponse(response []returnDataFormat) map[string][]returnDataFormat {
	newR := map[string][]returnDataFormat{}
	for _, data := range response {
		where := data.Where
		if _, ok := newR[where]; !ok {
			newR[where] = []returnDataFormat{data}
		} else {
			newR[where] = append(newR[where], data)
		}
	}
	return newR
}

func getNewData(w http.ResponseWriter, r *http.Request) {
	newChan := make(chan []returnDataFormat)
	for idx, data := range code {
		url := naverBase[idx]
		go getNewNaver(data, url, idx, newChan)
	}
	var response []returnDataFormat
	for range code {
		resp := <- newChan
		response = append(response, resp...)
	}
	close(newChan)

	newResponse := makeNewResponse(response)

	json.NewEncoder(w).Encode(newResponse)
}

func main() {
	fmt.Println("Hello World!")
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/new", getNewData).Methods("GET")
	log.Fatal(http.ListenAndServe(":1111", router))
}
