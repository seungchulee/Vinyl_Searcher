package service

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"

	"example.com/m/constant"
	"example.com/m/model"
)

func getNewNaver(code, url, where string, newChan chan []model.ReturnDataFormat) {
	var returns []model.ReturnDataFormat
	requestUrl := "https://smartstore.naver.com/i/v1/whole-products/" + code + "?sort=RECENT&mobile=false"
	resp, err := http.Get(requestUrl)
	if err != nil {
		log.Println(err)
	}

	respBody, _ := ioutil.ReadAll(resp.Body)
	var respData []model.RespUnit
	err = json.Unmarshal(respBody, &respData)
	if err != nil {
		log.Println("unmarshalling error")
	}
	for _, data := range respData {
		if data.SoldOut == "OUTOFSTOCK" {
			continue
		}
		returns = append(returns, model.ReturnDataFormat{
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

func makeNewResponse(response []model.ReturnDataFormat) map[string][]model.ReturnDataFormat {
	newR := map[string][]model.ReturnDataFormat{}
	for _, data := range response {
		where := data.Where
		if _, ok := newR[where]; !ok {
			newR[where] = []model.ReturnDataFormat{data}
		} else {
			newR[where] = append(newR[where], data)
		}
	}
	return newR
}

func GetNewData(w http.ResponseWriter, r *http.Request) {
	newChan := make(chan []model.ReturnDataFormat)

	for idx, data := range constant.CodeMap {
		url := constant.NaverAddr[idx]
		go getNewNaver(data, url, idx, newChan)
	}
	var response []model.ReturnDataFormat
	for range constant.CodeMap {
		resp := <-newChan
		response = append(response, resp...)
	}
	close(newChan)

	newResponse := makeNewResponse(response)

	err := json.NewEncoder(w).Encode(newResponse)
	if err != nil {
		log.Println(err)
	}
}
