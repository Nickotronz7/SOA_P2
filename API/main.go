package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"

	"database/sql"
	_ "github.com/go-sql-driver/mysql"
)

type record struct {
	Nombre_empleado string `json:"nombre"`
	Emocion         string `json:"emocion"`
}

var records []record
var db *sql.DB
var err error

func homePage(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hola Mundo")
	fmt.Println("Endpoint Hit: homePage")
}

func returnAllRecords(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Endpoint Hit: returnAllArticles")
	w.Header().Add("Content-Type", "JSON")
	json.NewEncoder(w).Encode(records)
}

func createNewRecord(w http.ResponseWriter, r *http.Request) {
	w.Header().Add("Content-Type", "JSON")
	reqBody, _ := ioutil.ReadAll(r.Body)
	var newRecord record
	json.Unmarshal(reqBody, &newRecord)

	records = append(records, newRecord)
	currentTime := time.Now()

	insert, err := db.Query("INSERT INTO EMPLEADO_EMOTIONS (create_time, name, emotion) VALUES ('"+currentTime.Format("2006.01.02 15:04:05")+"','"+newRecord.Nombre_empleado+"','"+newRecord.Emocion+"')")

	if err != nil {
		panic(err.Error())
	}

	defer insert.Close()

	json.NewEncoder(w).Encode(newRecord)

	
}

func handleRequests() {
	myRouter := mux.NewRouter().StrictSlash(true)
	
	myRouter.HandleFunc("/", homePage)
	myRouter.HandleFunc("/allrecords", returnAllRecords)
	myRouter.HandleFunc("/record", createNewRecord).Methods("POST")

	log.Fatal(http.ListenAndServe(":10000", myRouter))
}


func main() {
	
	// records = []record{
		// 	{Nombre_empleado: "Nicko", Emocion: "Feliz"},
		// 	{Nombre_empleado: "Chris", Emocion: "Pensativo"},
		// 	{Nombre_empleado: "Ulfran", Emocion: "Dudoso"},
		// }
		
	db, err = sql.Open("mysql", "emotionalUser:passwdEmotional@tcp(127.0.0.1:23306)/db_emotions")

	if err != nil {
		panic(err.Error())
	}

	defer db.Close()
	// fmt.Println("Exito")

	handleRequests()
}
