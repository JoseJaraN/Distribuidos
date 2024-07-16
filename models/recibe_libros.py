import pika
import json
from flask import Flask
from datetime import datetime
from config import DATABASE_CONNECTION_URI
from models.libro import Libro
from models.ordencompra import OrdenCompra
from models.detalleorden import DetalleOrden
from models.cliente import Cliente
from models.cobrar import Cobrar  # Asegúrate de importar el modelo Cobrar
from utils.db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 20
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 30
app.config["SQLALCHEMY_POOL_RECYCLE"] = 1800
db.init_app(app)

rabbitmq_host = 'localhost'
rabbitmq_request_queue = 'order_queue'
rabbitmq_response_queue = 'reserva_queue'
rabbitmq_user = 'grupo5'
rabbitmq_password = 'grupo5'

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

    try:
        # Parsear el mensaje
        message = json.loads(body.decode('utf-8'))
        dni = int(message['dni'])
        libros = message['libros']
        estado = int(message['estado'])  # Obtener el estado del mensaje


        # Verificar la cantidad en la base de datos y crear la orden de compra
        with app.app_context():
            cliente = Cliente.query.filter_by(dni=dni).first()
            print(f"Cliente: {cliente}")

            if not cliente:
                response_message = f"No se encontró el cliente con DNI: {dni}"
                send_response(response_message)
                return

            fecha_actual = datetime.now().date()
            hora_actual = datetime.now().time()

            total_precio = 0
            detalles = []
            for libro_data in libros:
                libro_id = int(libro_data['libroid'])
                cantidad = int(libro_data['cantidad'])

                libro = Libro.query.filter_by(libroid=libro_id).first()

                if libro:
                    if libro.cantidad >= cantidad:
                        total_precio += libro.precio * cantidad
                        detalles.append((libro_id, cantidad, libro.precio))
                        print(f"Libros disponibles")
                    else:
                        print(f"Libro ID: {libro_id} - No hay suficiente stock (disponible: {libro.cantidad}).")
                        return
                else:
                    response_message = f"Libro ID: {libro_id} no encontrado."
                    send_response(response_message)
                    return

            nueva_orden = OrdenCompra(clienteid=cliente.clienteid, fecha=fecha_actual, preciototal=total_precio, horapago=hora_actual)
            db.session.add(nueva_orden)
            db.session.commit()
            print(f"Nueva Orden: {nueva_orden}")

            for libro_id, cantidad, precio_unitario in detalles:
                detalle_orden = DetalleOrden(ordencompraid=nueva_orden.ordencompraid, libroid=libro_id, cantidad=cantidad, precio_unitario=precio_unitario)
                db.session.add(detalle_orden)
                libro = Libro.query.filter_by(libroid=libro_id).first()
                libro.cantidad -= cantidad
            db.session.commit()
            print("Cambios confirmados en la base de datos.")

            # Si el estado es 1, actualizar la tabla 'cobrar'
            if estado == 1:
                nuevo_cobro = Cobrar(clienteid=cliente.clienteid, ordencompraid=nueva_orden.ordencompraid, preciototal=total_precio)
                db.session.add(nuevo_cobro)
                db.session.commit()
                

            response_message = f"Enviar a Sist. reserva: Orden ID: {nueva_orden.ordencompraid}"
            print(response_message)
            send_response(response_message)
    except Exception as e:
        print(f"Error: {e}")

def send_response(response_message):
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Asegurarse de que la cola de respuesta existe
    channel.queue_declare(queue=rabbitmq_response_queue, durable=True)

    # Publicar la respuesta
    channel.basic_publish(exchange='', routing_key=rabbitmq_response_queue, body=str(response_message))
    connection.close()

def start_consuming():
    # Crear una conexión a RabbitMQ
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Asegurarse de que la cola de solicitud existe
    channel.queue_declare(queue=rabbitmq_request_queue, durable=True)

    # Configurar la cola para recibir mensajes
    channel.basic_consume(queue=rabbitmq_request_queue, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    start_consuming()