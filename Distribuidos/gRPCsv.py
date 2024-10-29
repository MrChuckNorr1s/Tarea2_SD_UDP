import grpc
from concurrent import futures
import pedidos_pb2
import pedidos_pb2_grpc
from statemachine import FiniteStateMachine, states
from confluent_kafka import Producer
import json
import time
import random
import threading
from uuid import uuid4
from datetime import datetime, timedelta

# Diccionario para almacenar el estado de cada pedido y su información
pedidos = {}

class GestorPedidos(pedidos_pb2_grpc.PedidosServicer):
    def RealizarPedido(self, request, context):
        pedido_id = str(uuid4())
        tiempo_estimado_entrega = random.randint(12, 20)

        # Guardar información del pedido, incluyendo el tiempo estimado y el tiempo inicial
        start_time = (datetime.now() - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
        pedidos[pedido_id] = {
            'fsm': FiniteStateMachine('Procesando', states),
            'producto': {
                'nombre_producto': request.nombre_producto,
                'precio': request.precio,
                'pasarela_pago': request.pasarela_pago,
                'email_cliente': request.email_cliente,
                'start_time': start_time,
                'estado_actual': 'Procesando',
                'tiempo_estimado_entrega': tiempo_estimado_entrega,
                'historial_estados': [('Procesando', start_time)]
            }
        }

        print(f"Pedido recibido: {request.nombre_producto}, ID: {pedido_id}, tiempo estimado: {tiempo_estimado_entrega}s")
        print(f"Start Time (Fecha legible ajustada): {start_time}")

        # Preparar mensaje inicial para Kafka
        pedido_data = pedidos[pedido_id]['producto']
        pedido_data['estado'] = 'Procesando'
        pedido_data['tiempo_estimado_entrega'] = tiempo_estimado_entrega

        producer = Producer({'bootstrap.servers': 'kafka1:9092'})
        producer.produce('el-topico1', key=pedido_id, value=json.dumps(pedido_data))
        producer.flush()

        # Publicar mensaje en el tópico de notificaciones para informar al cliente
        producer.produce('notificaciones', key=pedido_id, value=json.dumps({
            'pedido_id': pedido_id,
            'email_cliente': pedido_data['email_cliente'],
            'nombre_producto': pedido_data['nombre_producto'],
            'estado_actual': 'Procesando'
        }))
        producer.flush()

        # Iniciar hilo para cambiar estados automáticamente
        hilo = threading.Thread(target=self.cambiar_estados_automaticamente, args=(pedido_id,))
        hilo.start()

        return pedidos_pb2.PedidoResponse(mensaje="Pedido recibido y en estado Procesando")

    def cambiar_estados_automaticamente(self, pedido_id):
        producer = Producer({'bootstrap.servers': 'kafka1:9092'})
        while pedidos[pedido_id]['fsm'].state != 'Finalizado':
            try:
                tiempo_espera = random.randint(3, 7)
                time.sleep(tiempo_espera)

                # Cambiar al siguiente estado usando la máquina de estados
                nuevo_estado = pedidos[pedido_id]['fsm'].transition('next')
                producto_info = pedidos[pedido_id]['producto']

                # Actualizar el estado actual y agregar el timestamp ajustado
                producto_info['estado_actual'] = nuevo_estado
                timestamp_cambio = (datetime.now() - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
                producto_info['estado'] = nuevo_estado
                producto_info['historial_estados'].append((nuevo_estado, timestamp_cambio))

                print(f"Pedido {pedido_id} cambió a '{nuevo_estado}' en {timestamp_cambio}")

                # Enviar la nueva información a Kafka (para métricas)
                producer.produce('el-topico1', key=pedido_id, value=json.dumps(producto_info))
                
                # Publicar en el tópico de notificaciones para enviar un correo
                producer.produce('notificaciones', key=pedido_id, value=json.dumps({
                    'pedido_id': pedido_id,
                    'email_cliente': producto_info['email_cliente'],
                    'nombre_producto': producto_info['nombre_producto'],
                    'estado_actual': nuevo_estado
                }))
                producer.flush()

            except Exception as e:
                print(f"Error al cambiar el estado del pedido {pedido_id}: {e}")
                break

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pedidos_pb2_grpc.add_PedidosServicer_to_server(GestorPedidos(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC escuchando en el puerto 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

