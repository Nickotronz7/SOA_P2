package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"

	"github.com/gorilla/mux"

	"database/sql"

	_ "github.com/go-sql-driver/mysql"
)

type empleado struct {
	Nombre  string `json:"name"`
	Emocion string `json:"emotion"`
}
type record struct {
	Fecha     string     `json:"date"`
	Empleados []empleado `json:"employees"`
}

type dbRecord struct {
	Fecha           string `json:"fecha"`
	Nombre_empleado string `json:"nombre"`
	Emocion         string `json:"emocion"`
}

type response struct {
	Records []dbRecord `json:"response"`
}

var records []dbRecord
var db *sql.DB
var err error

func homePage(w http.ResponseWriter, _ *http.Request) {
	fmt.Fprintf(w, "Hola Mundo")
	fmt.Println("Endpoint Hit: homePage")
}

func returnAllRecords(w http.ResponseWriter, _ *http.Request) {
	w.Header().Add("Content-Type", "JSON")

	results, err := db.Query("SELECT create_time, name, emotion FROM EMPLEADO_EMOTIONS")

	if err != nil {
		panic(err.Error())
	}

	for results.Next() {
		var dbResponse dbRecord
		err = results.Scan(&dbResponse.Fecha,&dbResponse.Nombre_empleado,&dbResponse.Emocion)

		if err != nil {
			panic(err.Error())
		}

		records = append(records, dbResponse)
	}

	var finalResponse response

	finalResponse.Records = records

	json.NewEncoder(w).Encode(finalResponse)

	records = []dbRecord{}
}

func createNewRecord(w http.ResponseWriter, r *http.Request) {
	w.Header().Add("Content-Type", "JSON")
	reqBody, _ := ioutil.ReadAll(r.Body)
	var newRecord record
	err := json.Unmarshal(reqBody, &newRecord)

	if err != nil {
		panic(err.Error())
	}

	fecha_tmp := fixdate(strings.Split(newRecord.Fecha, "/"))
	var fecha string
	
	for f := 0; f < len(fecha_tmp); f++ {
		fecha = fecha + string(fecha_tmp[f])
	}

	var newEmpleado empleado
	for i := 0; i < len(newRecord.Empleados); i++ {
		newEmpleado = newRecord.Empleados[i]
		
		insert, err := db.Query("INSERT INTO EMPLEADO_EMOTIONS (create_time, name, emotion) VALUES ('" + fecha + "','" + newEmpleado.Nombre + "','" + newEmpleado.Emocion + "')")
		
		if err != nil {
			panic(err.Error())
		}

		defer insert.Close()
	}

	json.NewEncoder(w).Encode(newRecord)

	records = []dbRecord{}
}

func fixdate(input []string) []string {
	if (len(input) == 0) {
		return input
	}
	return append(fixdate(input[1:]), input[0])
}

func handleRequests() {
	myRouter := mux.NewRouter().StrictSlash(true)

	myRouter.HandleFunc("/", homePage)
	myRouter.HandleFunc("/allrecords", returnAllRecords)
	myRouter.HandleFunc("/record", createNewRecord).Methods("POST")

	log.Fatal(http.ListenAndServe(":10000", myRouter))
}

func main() {

	db, err = sql.Open("mysql", "emotionalUser:passwdEmotional@tcp(mysql_DB)/db_emotions")

	if err != nil {
		panic(err.Error())
	}

	defer db.Close()

	handleRequests()
}
