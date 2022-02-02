package main

import (
	"log"
	"net/http"
	_ "strings"

	"example.com/m/service"
	"github.com/gorilla/mux"
)

// main function
func main() {
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/api/new", service.GetNewData).Methods("GET")
	go http.ListenAndServe(":8080", nil)

	log.Fatal(http.ListenAndServe(":8080", router))
}
