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

// Estructura utilizada para asociar el nombre de un empleado con la emocion
type empleado struct {
	Nombre  string `json:"name"`
	Emocion string `json:"emotion"`
}

// Estructura utilizada para manejar los datos leidos de la cola
type record struct {
	Fecha     string     `json:"date"`
	Empleados []empleado `json:"employees"`
}

// Estructura utilizada para la insercion y lectura hacia la base de datos
type dbRecord struct {
	Fecha           string `json:"fecha"`
	Nombre_empleado string `json:"nombre"`
	Emocion         string `json:"emocion"`
}

// Estructura utilizada para manejar la respuesta total de la base de datos
// ya que como se hace un SELECT de 10 filas entonces la base de datos devuelve
// un array con las filas
type response struct {
	Records []dbRecord `json:"response"`
}

var records []dbRecord // Array de tipo dbRecord
var db *sql.DB // Puntero para manejar al conexion de la base de datos
var err error // Variable para la captura de errores
var rabbit_host = os.Getenv("RABBIT_HOST") // Direccion del host de rabbit
var rabbit_port = os.Getenv("RABBIT_PORT") // Puerto expuesto por rabbit
var rabbit_queue = os.Getenv("RABBIT_CONSUMER_QUEUE") // Nombre de la cola

// Funcion que maneja solicitudes que llegan a la raiz del endpoint
func homePage(w http.ResponseWriter, _ *http.Request) {
	fmt.Fprintf(w, "Hola Mundo")
	fmt.Println("Endpoint Hit: homePage")
}

// Funcion para habilitar los CORS en el request
func enableCors(w* http.ResponseWriter) {
	(*w).Header().Set("Access-Control-Allow-Origin", "*")
}

// Funcion que maneja los request del ResultsUI
func returnAllRecords(w http.ResponseWriter, _ *http.Request) {
	enableCors(&w) // Se habilita CORS en el request
	w.Header().Add("Content-Type", "JSON") // Se añade el header de content-type JSON

	results, err := db.Query("SELECT create_time, name, emotion FROM EMPLEADO_EMOTIONS") // se envia un request a la base de datos para obtener los datos almacenados

	// Se verifica si hubo un error en el request hacia la base de datos
	if err != nil {
		panic(err.Error())
	}

	// Se itera sobre los elementos de la respuesta de la base de datos
	for results.Next() {
		var dbResponse dbRecord // Variable temporal para almacernar la fila correspondiente a la iteracion
		err = results.Scan(&dbResponse.Fecha, &dbResponse.Nombre_empleado, &dbResponse.Emocion) // Mapeo de cada columna de la iteracion hacia la variable dbRecord

		// Se verifica si hubo un error en la asignacion de los valores de la respuesta de la base de datos en la variable dbRecord
		if err != nil {
			panic(err.Error())
		}

		records = append(records, dbResponse) // Se añade al array de resultados
	}

	var finalResponse response // Variable para almacenar la respuesta que sera retornada hacia ResultsUI

	finalResponse.Records = records // Incorporacion de los records de la base de datos en la respuesta final

	json.NewEncoder(w).Encode(finalResponse) // Parseo de la respuesta en formato JSON

	fmt.Println("Responded to resultsUI") // Print de loggeo

	records = []dbRecord{} // Limpieza del array de records
}

// Funcino para insertar datos en la base de datos
func createNewRecord(msg []byte) {
	var newRecord record // Variable para estructurar los datos recibidos
	err := json.Unmarshal(msg, &newRecord) // Mapeo del JSON recibido en la estructura record

	// Se verifica si hubo un error en el Mapeo del JSON recibido
	if err != nil {
		panic(err.Error())
	}

	fecha_tmp := fixdate(strings.Split(newRecord.Fecha, "/")) // Se llama a la funcion que le da vuelta a al fecha del JSON recibido y se divide la fecha usando el caracter '/'
	var fecha string // Variable en la que se almacena la fecha cuando este corregida

	// Se juntan las partes de la fecha 
	for f := 0; f < len(fecha_tmp); f++ {
		fecha = fecha + string(fecha_tmp[f])
	}

	var newEmpleado empleado // Variable para estructurar la informacion de cada empleado
	// Se itera sobre cada elemento de los datos leidos de la cola para insertar en la base de datos
	for i := 0; i < len(newRecord.Empleados); i++ {
		newEmpleado = newRecord.Empleados[i] // se crea un objeto empleado

		insert, err := db.Query("INSERT INTO EMPLEADO_EMOTIONS (create_time, name, emotion) VALUES ('" + fecha + "','" + newEmpleado.Nombre + "','" + newEmpleado.Emocion + "')") // Se insertan los datos en la base de datos

		// Se verifica se hubo un error en la insercino de datos
		if err != nil {
			panic(err.Error())
		}

		fmt.Println("Insertado record bien") // Print de control

		defer insert.Close() // Se cierra el canal de insecion, cuando la funcion 'createNewRecord' haga return
	}
}

// Funcion que arregla la fecha recibida, este arreglo consiste en invertir el orden ya que la fecha llega con el formato dd/mm/yyyy
func fixdate(input []string) []string {
	if len(input) == 0 {
		return input
	}
	return append(fixdate(input[1:]), input[0]) // Llamada recursiva para la inversion de la lista
}

// Funcion que se encarga de manejar las diferentes solicitudes http que se reciben
func handleRequests() {
	myRouter := mux.NewRouter().StrictSlash(true) // Se crea un nuevo router para el direccionamiento 

	myRouter.HandleFunc("/", homePage) // Ruteo de los request que llegan a '/'
	myRouter.HandleFunc("/allrecords", returnAllRecords) // Ruteo de las solicitudes que llegan a la ruta '/'

	log.Fatal(http.ListenAndServe(":10000", myRouter)) // Exposicion del puerto para el servidor
}

// Funcion que se encarga de la creacion de la cola a escuchar
func process_consumer() {
	conn, err := amqp.Dial("amqp://guest:guest@" + rabbit_host + ":" + rabbit_port + "/") // Conexion al servicio de RabbitMQ

	// Verificacion si hubo un error al conectarse al servicio de rabbitMQ
	if err != nil {
		log.Fatalf("%s: %s", "Failed to connect to RabbitMQ", err)
	}

	ch, err := conn.Channel() // Apertura con el canal del rabbitMQ

	// Verificacion si hubo un error en la apertura del canal
	if err != nil {
		log.Fatal("%s: %s", "Failed to open a channel", err)
	}

	// Declaracion de la cola en el canal
	q, err := ch.QueueDeclare(
		rabbit_queue, // queue name
		false,         // duarable
		false,        // delete when unused
		false,        // exclusive
		false,        // no-wait
		nil,          //arguments

	)

	// Verificacion si hubo un error en la declaracion de la cola
	if err != nil {
		log.Fatalf("%s: %s", "Failed to declare a queue", err)
	}

	fmt.Println("Queue and Channel established") // Print de control

	defer conn.Close() // Se crea una peticion de clausura de la conexion que se ejecutara cuando la funcion 'process_consumer' haga return
	defer ch.Close() // Se crea una peticion de clausura del canal que se ejecutara cuando la funcion 'process_consumer' haga return

	// Definicion del comportamiento con respecto al canal, en este caso es de consumo
	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		false,  // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)

	// Se verifica si ha habido un error en el registro del consumidor en el canal
	if err != nil {
		log.Fatalf("%s: %s", "Failed to register consumer", err)
	}

	forever := make(chan bool) // Se crea una etiquet y se inicializa el objeto chan

	// Se hace un hold esperando a que se lean mensajes de la cola
	go func ()  {
		// Cuando se lee un mensaje de la cola este se recibe y se empiza a manipular para insertar los datos en la base de datos
		for d := range msgs {
			log.Printf("Recived a message: %d", len(d.Body)) // Print de control
			d.Ack(true) // se hace acknowledge del mensaje
			createNewRecord(d.Body) // se llama a la funcion encargada de ingresar los datos en la base de datos
		}
	} ()

	fmt.Println("Running") // print de control
	<-forever // Se salta a la etiqueta 'forever' para escuchar nuevamente por mensajes en la cola
}

// Funcion principal del programa
func main() {

	db, err = sql.Open("mysql", "emotionalUser:passwdEmotional@tcp(db-service)/db_emotions") // Se abre una conexion con la base de datos 'db_emotions

	// Verificacion de error en la conexion de la base de datos
	if err != nil {
		panic(err.Error())
	}

	fmt.Println("Connected to DB") // Print de control

	defer db.Close() // Se crea una peticion de clausura de la conexion 

	// Creacion de la tabla de 'EMPLEADO_EMOTIONS' en caso de que no exista
	_, err := db.Exec("CREATE TABLE IF NOT EXISTS EMPLEADO_EMOTIONS(id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key', create_time DATETIME COMMENT 'Create Time', name VARCHAR(255), emotion VARCHAR(255))")

	// Verificacion de error en la creacion de la tabla
	if err != nil {
		panic(err.Error())
	}

	fmt.Println("Table created") // Print de control

	go process_consumer() // Creacion de un thread para el manejo del canal

	handleRequests() // Llamado de la funcion para el manejo de las peticiones http
}
