package main

import (
	"log"
	"net/http"
	_ "strings"

	"example.com/m/service"
	"github.com/gorilla/mux"
)

func main() {
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/new", service.GetNewData).Methods("GET")
	log.Fatal(http.ListenAndServe(":1111", router))
}
