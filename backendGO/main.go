package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"
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
	"월간바이닐":     "https://smartstore.naver.com/allthatvinyl",
	"뮤니버스24":    "https://smartstore.naver.com/muniverse24",
	"스피츠레코드":    "https://smartstore.naver.com/spitzrecords",
	"미드나잇스낵":    "https://smartstore.naver.com/midnightsnack",
	"신나라레코드":    "https://smartstore.naver.com/synnara-nshop",
}

var code = map[string]string{
	"기기레코즈":     "100632872",
	"바이닐코리아":    "100599518",
	"마이페이보릿스토어": "100517823",
	"하이닐":       "100797246",
	"테리픽잼":      "100710783",
	"레코드스톡":     "100804461",
	"라보앤드":      "100078012",
	"마뮤":        "100787591",
	"판다바이닐":     "100975984",
	"뮤직랜드":      "500015866",
	"구해줘굿즈":     "100610551",
	"라운드뮤직":     "100747626",
	"인펙션스 레코드":  "100619159",
	"비트볼 뮤직":    "500280301",
	"서울 바이닐":    "100129192",
	"서울 레코드":    "500173380",
	"사운드룩":      "500017851",
	"드림 레코드":    "100116811",
	"바이닐 앤 바이브": "101150414",
	"아이러브뮤직":    "100239915",
	"슬로우바이닐":    "100795359",
	"월간바이닐":     "100863912",
	"뮤니버스24":    "100871676",
	"스피츠레코드":    "100994334",
	"미드나잇스낵":    "101165512",
	"신나라레코드":    "500004749",
}

type respUnit struct {
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
	requestUrl := "https://smartstore.naver.com/i/v1/whole-products/" + code + "?sort=RECENT&mobile=false"
	resp, err := http.Get(requestUrl)
	if err != nil {
		log.Println(err)
	}

	respBody, _ := ioutil.ReadAll(resp.Body)
	var respData []respUnit
	err = json.Unmarshal(respBody, &respData)
	if err != nil {
		log.Println("unmarshalling error")
	}
	for _, data := range respData {
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
		resp := <-newChan
		response = append(response, resp...)
	}
	close(newChan)

	newResponse := makeNewResponse(response)

	json.NewEncoder(w).Encode(newResponse)
}

func main() {
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/new", getNewData).Methods("GET")
	log.Fatal(http.ListenAndServe(":1111", router))
}
