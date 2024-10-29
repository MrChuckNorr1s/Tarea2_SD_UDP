# Sistemas Distribuidos
> Tarea 2: Sistema para la Gestión Logística en una Aplicación de Ecommerce


## General Information
- Este proyecto implementa un sistema distribuido capaz de gestionar y monitorear el estado de los pedidos realizados a través del ecommerce de una gran tienda de retail.
- Luego de establecer la conexión se planea analizar los distintos escenarios que se piden en la tarea.


<!-- You don't have to answer all the questions - just the ones relevant to your project. -->


## Technologies Used
- Terminal Ubuntu 22.04
- Cliente y Servidor gRPC.
- Python-3 o superior, con sus dependencias.
- Apache Kafka
- ElasticSearch
- Kibana
- Apache ZooKeeper
- Contenedores Docker

## Setup
Descargar la carpeta **Distribuidos** para tener todos los archivos necesarios para levantar el sistema caché.

Antes de establecer la conexión entre los contenedores, se crea el archivo docker-compose.yml, la cual se encarga de hacer correr los múltiples contenedores de Docker para así facilitar el despliegue de los servicios del sistema, asegurando que se inicien, se conecten entre sí a través de una red común y se mantengan operativos.

Se crean los contenedores descritos en el docker-compose.yml:
```diff
sudo docker-compose up --build -d
```
Luego, se comprueba que todos los contenedores estén funcionando con el comando:
```diff
sudo docker-compose ps
```
Si los contenedores están con estatus **up**, se procede a seguir, pero si el contenedor de **Kafka Topic** está con estatus **exit 1**, entonces se ejecuta el archivo **KafkaTopic.py** para crear el tópico:
```diff
python3 kafkaTopic.py
```
Luego se procede a generar los pedidos.

## Usage

Para correr el sistema, simplementa se utiliza el comando **python3** para iniciar el generador de pedidos, la cual es el cliente de gRPC.

```diff
python3 gRPCcli.py
```
Al mismo tiempo en otra terminal, se ejecuta el archivo **consumer.py** para ir enviando las métricas a Elastic Search y así poder graficar los resultados obtenidos.
```diff
python3 consumer.py
```
Para visualizar los resultados en el **UI de Kafka**, en un navegador se usa:
```diff
localhost:8080
```
Y para ver los resultados para graficar en Elastic Search, se busca en el navegador:
```diff
localhost:5601
```
Finalmente, para cambiar las distribuciones de carga, simplemente hay que insertarlo al ejecutar el cliente gRPC.
