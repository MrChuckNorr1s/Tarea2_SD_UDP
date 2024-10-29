from confluent_kafka import Consumer
from elasticsearch import Elasticsearch
import json
import time
from datetime import datetime

# Configuración de Elasticsearch
es = Elasticsearch([{'scheme': 'http', 'host': 'localhost', 'port': 9200}])

def enviar_latencia_elasticsearch(latencia_por_estado, pedido_data):
    doc = {
        'latencia_por_estado': latencia_por_estado,
        'pedido_data': pedido_data,
        'timestamp': time.time()
    }
    try:
        response = es.index(index="latencias-pedidos", body=doc)
        print(f"Documento de latencia enviado a Elasticsearch: {response['result']}")
    except Exception as e:
        print(f"Error al enviar el documento de latencia a Elasticsearch: {e}")

def enviar_throughput_elasticsearch(throughput):
    doc = {
        'throughput': throughput,
        'timestamp': time.time()
    }
    try:
        response = es.index(index="metricas-throughput", body=doc)
        print(f"Documento de throughput enviado a Elasticsearch: {response['result']}")
    except Exception as e:
        print(f"Error al enviar el documento de throughput a Elasticsearch: {e}")

def enviar_tiempo_real_entrega(tiempo_real_entrega, tiempo_estimado_entrega, pedido_data):
    doc = {
        'tiempo_real_entrega': tiempo_real_entrega / 1000,  # Convertir a segundos si prefieres
        'tiempo_estimado_entrega': tiempo_estimado_entrega,
        'pedido_id': pedido_data.get('pedido_id'),
        'timestamp': time.time()
    }
    try:
        response = es.index(index="tiempos-entrega", body=doc)
        print(f"Documento de tiempo de entrega enviado a Elasticsearch: {response['result']}")
    except Exception as e:
        print(f"Error al enviar el documento de tiempo de entrega a Elasticsearch: {e}")

# Configuración del consumidor Kafka
consumer_conf = {
    'bootstrap.servers': 'localhost:9093',
    'group.id': 'grupo-consumidor1',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_conf)
consumer.subscribe(['el-topico1'])

contador_pedidos = 0
start_time_throughput = time.time()
ventana_tiempo = 60
max_mensajes = 100
tiempo_maximo = 300
start_time = time.time()

try:
    while contador_pedidos < max_mensajes and (time.time() - start_time) < tiempo_maximo:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            print(f"Error del consumidor: {msg.error()}")
            continue

        message_key = msg.key().decode('utf-8')
        message_value = msg.value().decode('utf-8')
        pedido_data = json.loads(message_value)

        print(f"\nMensaje recibido - Pedido: {pedido_data.get('nombre_producto')}")
        print(json.dumps(pedido_data, indent=4, ensure_ascii=False))

        # Calcular latencia por estado para este pedido
        historial_estados = pedido_data.get('historial_estados', [])
        latencia_por_estado = {}
        tiempo_real_entrega = 0  # Inicializar el tiempo real de entrega como la suma de latencias
        if historial_estados:
            for i in range(1, len(historial_estados)):
                estado_anterior, fecha_anterior = historial_estados[i - 1]
                estado_actual, fecha_actual = historial_estados[i]
                timestamp_anterior = datetime.strptime(fecha_anterior, '%Y-%m-%d %H:%M:%S').timestamp()
                timestamp_actual = datetime.strptime(fecha_actual, '%Y-%m-%d %H:%M:%S').timestamp()

                # Calcular latencia entre estados en milisegundos
                latencia = (timestamp_actual - timestamp_anterior) * 1000
                latencia_por_estado[f"{estado_anterior}_a_{estado_actual}"] = latencia

                # Acumular latencia para obtener el tiempo real de entrega
                tiempo_real_entrega += latencia

        # Si el pedido está finalizado, envía latencia y tiempo real de entrega
        if pedido_data['estado'] == 'Finalizado':
            contador_pedidos += 1
            enviar_latencia_elasticsearch(latencia_por_estado, pedido_data)

            # Obtener el tiempo estimado de entrega y enviar el tiempo real y estimado a Elasticsearch
            tiempo_estimado_entrega = pedido_data.get("tiempo_estimado_entrega", 0)
            enviar_tiempo_real_entrega(tiempo_real_entrega, tiempo_estimado_entrega, pedido_data)

        # Calcular y enviar throughput al final de la ventana de tiempo
        if (time.time() - start_time_throughput) >= ventana_tiempo:
            throughput = contador_pedidos / (ventana_tiempo / 60.0)
            print(f"\n[THROUGHPUT] Throughput actual: {throughput:.2f} pedidos/minuto\n")
            enviar_throughput_elasticsearch(throughput)
            contador_pedidos = 0
            start_time_throughput = time.time()

finally:
    if contador_pedidos > 0:
        throughput = contador_pedidos / ((time.time() - start_time_throughput) / 60.0)
        print(f"\n[THROUGHPUT FINAL] Throughput final: {throughput:.2f} pedidos/minuto\n")
        enviar_throughput_elasticsearch(throughput)

    consumer.close()
    print("Proceso de consumo completado.")


