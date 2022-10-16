SOA_P2 es una aplicación de microservicios con componentes web para la interacción del usuario. La aplicación web le permite al usuario seleccionar las imagenes de las personas a las que se les debe generar el análisis de las emociones y también observar el resultado final.

Los servicios están almacenados en contenedores utilizando Docker que a su vez son administrados utilizando minikube el cual implementa un cluster de Kuberntetes. 

Entre los servicios se encuentran:

AddUI: Es el servicio con el que interactúa el usuario. Permite enviar imágenes al sistema para ser analizado. Se utiliza como una aplicación web, ejecutando el pod que la contiene y accediendo desde un navegador

Pasos para su implementación
1. Clonar el repositorio:

git clone https://github.com/Nickotronz7/SOA_P2.git

Se deben seguir los siguientes comandos para el despliegue del minikube de Kubernetes. 
Nota: Asegurarse que el direcctorio de la consola se encuentra en la raiz del repositorio
Nota: Asegurarse que está autenticado con el proyecto de emotions service en GCP, puede utilizar este comando para hacerlo (gcloud auth application-default login)

2. minikube start

3. minikube addons enable gcp-auth

4. kubectl create ns rabbits

5. kubectl apply -n rabbits -f k8s_apply

6. kubectl -n rabbits get pods

7. kubectl -n rabbits port-forward rabbitmq-0 15672:15672

8. kubectl -n rabbits port-forward deployment/backend-service 10000:10000

9. kubectl -n rabbits port-forward deployment/resultsui-service 3000:3000

10. kubectl -n rabbits port-forward deployment/addui-service 5000:5000

11. Para acceder a los componentes con interfaz debe ingresar como url en el navegador las siguientes direcciones:

- http://localhost:15672
- http://localhost:5000
- http://localhost:3000
