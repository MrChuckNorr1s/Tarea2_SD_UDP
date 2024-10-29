import grpc
import random
import pedidos_pb2
import pedidos_pb2_grpc

# Listas de valores para seleccionar aleatoriamente
productos = ["Laptop", "Teléfono", "Tablet", "Monitor", "Teclado"]
precios = [1000.0, 1200.0, 800.0, 1500.0, 600.0]
pasarelas_pago = ["MercadoPago", "Webpay", "EtPay", "Kiphu"]
marcas_tarjeta = ["VISA", "Mastercard", "AMEX"]
bancos = ["BancoEstado", "Santander", "BCI"]
regiones = ["Región Metropolitana", "Valparaíso", "Concepción"]
direcciones = ["Avenida Siempre Viva 123", "Calle Falsa 456", "Boulevard de los Sueños 789"]
emails = ["xcristianx5569@gmail.com"]

def realizar_pedido():
    # Conectar con el servidor gRPC
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pedidos_pb2_grpc.PedidosStub(channel)

        try:
            # Seleccionar valores aleatorios de las listas
            nombre_producto = random.choice(productos)
            precio = random.choice(precios)
            pasarela_pago = random.choice(pasarelas_pago)
            marca_tarjeta = random.choice(marcas_tarjeta)
            banco = random.choice(bancos)
            region_envio = random.choice(regiones)
            direccion_envio = random.choice(direcciones)
            email_cliente = random.choice(emails)

            # Crear la solicitud de pedido con los valores aleatorios
            pedido = pedidos_pb2.PedidoRequest(
                nombre_producto=nombre_producto,
                precio=precio,
                pasarela_pago=pasarela_pago,
                marca_tarjeta=marca_tarjeta,
                banco=banco,
                region_envio=region_envio,
                direccion_envio=direccion_envio,
                email_cliente=email_cliente
            )

            # Enviar la solicitud al servidor y obtener una respuesta
            response = stub.RealizarPedido(pedido)
            print(f"Pedido: {nombre_producto}, Precio: {precio}, Pasarela: {pasarela_pago}")
            print(f"Respuesta del servidor: {response.mensaje}")

        except grpc.RpcError as e:
            print(f"Error en la conexión gRPC: {e.details()}")
            print(f"Código de estado: {e.code()}")

def enviar_pedidos(cantidad_pedidos):
    for _ in range(cantidad_pedidos):
        realizar_pedido()

if __name__ == "__main__":
    # Solicitar al usuario la cantidad de pedidos a enviar
    try:
        cantidad = int(input("Ingrese la cantidad de pedidos a enviar: "))
        enviar_pedidos(cantidad)
    except ValueError:
        print("Por favor, ingrese un número válido.")


