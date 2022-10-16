package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"

	"github.com/gorilla/mux"

	"database/sql"

	_ "github.com/go-sql-driver/mysql"

	log "github.com/sirupsen/logrus"
	"github.com/streadway/amqp"
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
var rabbit_host = os.Getenv("RABBIT_HOST")
var rabbit_port = os.Getenv("RABBIT_PORT")
var rabbit_queue = os.Getenv("RABBIT_CONSUMER_QUEUE")

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
		err = results.Scan(&dbResponse.Fecha, &dbResponse.Nombre_empleado, &dbResponse.Emocion)

		if err != nil {
			panic(err.Error())
		}

		records = append(records, dbResponse)
	}

	var finalResponse response

	finalResponse.Records = records

	json.NewEncoder(w).Encode(finalResponse)

	fmt.Println("Responded to resultsUI")

	records = []dbRecord{}
}

func createNewRecord(msg []byte) {
	// w.Header().Add("Content-Type", "JSON")
	// reqBody, _ := ioutil.ReadAll(r.Body)
	// err := json.Unmarshal(reqBody, &newRecord)
	var newRecord record
	err := json.Unmarshal(msg, &newRecord)

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

		fmt.Println("Insertado record bien")
		defer insert.Close()
	}
}

func fixdate(input []string) []string {
	if len(input) == 0 {
		return input
	}
	return append(fixdate(input[1:]), input[0])
}

func handleRequests() {
	myRouter := mux.NewRouter().StrictSlash(true)

	myRouter.HandleFunc("/", homePage)
	myRouter.HandleFunc("/allrecords", returnAllRecords)
	// myRouter.HandleFunc("/record", createNewRecord).Methods("POST")go get github.com/streadway/amqp

	log.Fatal(http.ListenAndServe(":10000", myRouter))
}

func process_consumer() {
	conn, err := amqp.Dial("amqp://guest:guest@" + rabbit_host + ":" + rabbit_port + "/")
	if err != nil {
		log.Fatalf("%s: %s", "Failed to connect to RabbitMQ", err)
	}

	ch, err := conn.Channel()
	if err != nil {
		log.Fatal("%s: %s", "Failed to open a channel", err)
	}

	q, err := ch.QueueDeclare(
		rabbit_queue, // queue name
		false,         // duarable
		false,        // delete when unused
		false,        // exclusive
		false,        // no-wait
		nil,          //arguments

	)
	if err != nil {
		log.Fatalf("%s: %s", "Failed to declare a queue", err)
	}

	fmt.Println("Queue and Channel established")

	defer conn.Close()
	defer ch.Close()

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		false,  // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	if err != nil {
		log.Fatalf("%s: %s", "Failed to register consumer", err)
	}

	forever := make(chan bool)

	go func ()  {
		for d := range msgs {
			log.Printf("Recived a message: %d", len(d.Body))
			d.Ack(true)
			createNewRecord(d.Body)
		}
	} ()

	fmt.Println("Running")
	<-forever
}

func main() {

	db, err = sql.Open("mysql", "emotionalUser:passwdEmotional@tcp(db-service)/db_emotions")
	if err != nil {
		panic(err.Error())
	}
	fmt.Println("Connected to DB")

	defer db.Close()

	_, err := db.Exec("CREATE TABLE IF NOT EXISTS EMPLEADO_EMOTIONS(id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key', create_time DATETIME COMMENT 'Create Time', name VARCHAR(255), emotion VARCHAR(255))")
	if err != nil {
		panic(err.Error())
	}
	fmt.Println("Table created")

	go process_consumer()
	handleRequests()
}
