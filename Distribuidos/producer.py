from confluent_kafka import Producer
from elasticsearch import Elasticsearch
import time
import json
from uuid import uuid4

# Configuración de Elasticsearch
es = Elasticsearch([{'scheme': 'http', 'host': 'localhost', 'port': 9200}])

# Configura el Producer para conectarse a los brokers de Kafka
producer_conf = {
    'bootstrap.servers': 'localhost:9093',
    'client.id': 'productor1'
}
producer = Producer(producer_conf)

def enviar_metrica_elasticsearch(latencia, throughput):
    doc = {
        'latencia': latencia,  # En milisegundos
        'throughput': throughput,  # Número de mensajes por minuto
        'timestamp': time.time(),
    }
    es.index(index="metricas-pedidos", body=doc)

def delivery_report(err, msg):
    if err is not None:
        print(f"Error al entregar mensaje: {err}")
    else:
        print(f"Mensaje enviado a {msg.topic()} [{msg.partition()}]")

# Ejemplo de envío de 100 mensajes con registro de métricas
for i in range(100):
    start_time = time.time()  # Marca de tiempo inicial

    # Datos del pedido que se envía
    data = {
        'nombre_producto': f'Producto {i}',
        'precio': 100 + i,
        'pasarela_pago': 'MercadoPago',
        'marca_tarjeta': 'VISA',
        'banco': 'Banco Estado',
        'region_envio': 'Región Metropolitana',
        'direccion_envio': 'Calle 123',
        'email_cliente': 'cliente@correo.com'
    }

    message = json.dumps(data)
    producer.produce('el-topico1', key=str(uuid4()), value=message, callback=delivery_report)

    producer.poll(0)

    # Calcular latencia
    end_time = time.time()
    latencia = (end_time - start_time) * 1000  # Latencia en milisegundos

    # Simula el throughput como 1 mensaje procesado por este ciclo
    throughput = 1

    # Enviar las métricas a Elasticsearch
    enviar_metrica_elasticsearch(latencia, throughput)

    time.sleep(1)  # Simula una pausa de 1 segundo entre envíos

# Espera a que todos los mensajes pendientes sean entregados
producer.flush()



