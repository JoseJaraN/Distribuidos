from flask import Blueprint, jsonify
from models.cliente import Cliente
from models.libro import Libro
from models.detalleorden import DetalleOrden
from models.cobrar import Cobrar

data_bp = Blueprint('data', __name__)

@data_bp.route('/enviarDatos', methods=['GET'])
def datos():
    try:
        # Obtener todos los registros de la tabla Cobrar
        cobros = Cobrar.query.all()
        cobros_data = []

        for cobro in cobros:
            # Obtener el nombre del cliente
            cliente = Cliente.query.filter_by(clienteid=cobro.clienteid).first()
            nombre_cliente = cliente.nombre if cliente else "Cliente no encontrado"

            # Obtener los detalles de la orden
            detalles_orden = DetalleOrden.query.filter_by(ordencompraid=cobro.ordencompraid).all()
            lista_libros = []

            for detalle in detalles_orden:
                # Obtener los detalles del libro
                libro = Libro.query.filter_by(libroid=detalle.libroid).first()
                if libro:
                    lista_libros.append({
                        'nombre_libro': libro.nombre,
                        'cantidad': detalle.cantidad,
                        'precio_unitario': detalle.precio_unitario
                    })

            cobros_data.append({
                'nombre_cliente': nombre_cliente,
                'libros': lista_libros,
                'preciototal': cobro.preciototal
            })

        data = {
            'message': 'Lista de cobros con detalles de libros',
            'status': 200,
            'datos': cobros_data,
        }

        return jsonify(data), 200

    except Exception as e:
        return jsonify({'message': 'Error al obtener los datos', 'error': str(e)}), 500
