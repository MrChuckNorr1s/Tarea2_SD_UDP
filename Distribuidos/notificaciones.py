from confluent_kafka import Consumer
import json
import smtplib
from email.mime.text import MIMEText

# Función para enviar correos electrónicos
def enviar_email(destinatario, asunto, cuerpo):
    # Configuración de las credenciales de Gmail
    email_user = 'juanitocalvino123@gmail.com'  # Correo emisor
    email_password = 'ezkd djoi oapw qshl'  # Contraseña de aplicación

    # Configurar el contenido del correo
    msg = MIMEText(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = email_user
    msg['To'] = destinatario

    try:
        # Conectar al servidor SMTP de Gmail
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Iniciar la conexión TLS
            server.login(email_user, email_password)  # Autenticación
            server.send_message(msg)  # Enviar el mensaje
            print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error enviando correo: {e}")

# Función para manejar y enviar la notificación de cambio de estado
def notificar_estado_pedido(email_cliente, nuevo_estado, nombre_producto):
    asunto = "Actualización de estado de tu pedido"
    cuerpo = f"Tu pedido de {nombre_producto} ha cambiado al estado: {nuevo_estado}."
    print(f"Intentando enviar correo a {email_cliente} sobre el estado {nuevo_estado}")
    enviar_email(email_cliente, asunto, cuerpo)

# Configuración del consumidor Kafka para el microservicio de notificaciones
consumer_conf = {
    'bootstrap.servers': 'kafka1:9092',
    'group.id': 'grupo-notificaciones',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_conf)
consumer.subscribe(['notificaciones'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error del consumidor: {msg.error()}")
            continue

        # Procesar el mensaje de cambio de estado recibido de Kafka
        message_value = msg.value().decode('utf-8')
        notification_data = json.loads(message_value)
        
        # Extraer los datos necesarios para la notificación
        email_cliente = notification_data['email_cliente']
        nombre_producto = notification_data['nombre_producto']
        estado_actual = notification_data['estado_actual']
        
        # Enviar la notificación por correo electrónico
        notificar_estado_pedido(email_cliente, estado_actual, nombre_producto)

finally:
    consumer.close()

