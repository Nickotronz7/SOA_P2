# SOA_P2

SOA_P2 es una aplicación de microservicios con componentes web para la interacción del usuario. La aplicación web le permite al usuario seleccionar las imagenes de las personas a las que se les debe generar el análisis de las emociones y también observar el resultado final.

Los servicios están almacenados en contenedores utilizando Docker que a su vez son administrados utilizando minikube el cual implementa un cluster de Kuberntetes. 

Entre los servicios se encuentran:

Pasos para su implementación
1. Clonar el repositorio:

`git clone https://github.com/Nickotronz7/SOA_P2.git`

Se deben seguir los siguientes comandos para el despliegue del minikube de Kubernetes. 
Nota: Asegurarse que el direcctorio de la consola se encuentra en la raiz del repositorio
Nota: Asegurarse que está autenticado con el proyecto de emotions service en GCP, puede utilizar este comando para hacerlo (gcloud auth application-default login)

2. Inicial minikube

  `minikube start`

3. Habilitar el addon para el uso de credenciales con el API de google

  `minikube addons enable gcp-auth`

4. Crear de un namespace

  `kubectl create ns rabbits`

5. Hacer una apply

  `kubectl apply -n rabbits -f k8s_apply`

6. Verfiicar el estado de los pods

  `kubectl -n rabbits get pods`

7. Exponer puertos para el dashboard de rabbit

  `kubectl -n rabbits port-forward rabbitmq-0 15672:15672`

8. Habilitar puertos del backend

  `kubectl -n rabbits port-forward deployment/backend-service 10000:10000`

9. Habilitar puertos del resultui

  `kubectl -n rabbits port-forward deployment/resultsui-service 3000:3000`

10. Habilitar puertos del resultui

  `kubectl -n rabbits port-forward deployment/addui-service 5000:5000`

11. Para acceder a los componentes con interfaz debe ingresar como url en el navegador las siguientes direcciones:

- http://localhost:15672
- http://localhost:5000
- http://localhost:3000

## Servicios de SOA_P2
| Servicio | Lenguaje | Description |
|----------|----------|-------------|
|AddUI|Python|Es una interfaz que permite al usuario seleccionar las 10 imagenes que requieren ser procesadas por el servicio Emotions|
|Database|MySQL|Se encarga del almacenamiento de los datos de los empleado, sus nombre, emocion y la fecha que corresponda|
|Backend|Go|Funciona como intermediario para poder almacenar en la base de datos toda la informacion ya analizada por el servicio de emotions y a su vez preveer esta informacion a ResultsUI|
|Emotions|Python|Analiza las imagenes que recibe como entrada y dermina la emocion que refleja cada persona|
|Broker|RabbitMQ, Docker Image|Su funcion es mantener las conexiones y controlar el trafico de datos por medio de mensajes asincronicos|
|ResultsUI|React|Se encarga de desplegar los datos referentes a los empleados una vez ya han sido analizados. Este servicio genera solicitudes HTTP GET al backend|
