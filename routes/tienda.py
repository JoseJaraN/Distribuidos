from flask import Blueprint, jsonify
from models.cliente import Cliente
from models.libro import Libro

data_bp = Blueprint('data', __name__)

@data_bp.route('/enviarDatos', methods=['GET'])
def datos():
    try:
        # Obtener todas las áreas
        clientes = Cliente.query.all()
        dato_cliente = [cliente.serialize() for cliente in clientes]
        
        # Obtener todos los horarios
        libros = Libro.query.all()
        lista_libros = [libro.serialize() for libro in libros]
        
        data = {
            'message': 'Lista de áreas y horarios',
            'status': 200,
            'dato': dato_cliente,
            'libros': lista_libros,
        }
        
        return jsonify(data), 200

    except Exception as e:
        return jsonify({'message': 'Error al obtener áreas y horarios', 'error': str(e)}), 500