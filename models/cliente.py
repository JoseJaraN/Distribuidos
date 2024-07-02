from utils.db import db

class Cliente(db.Model):
    __tablename__ = 'cliente'
    clienteid = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer)
    nombre = db.Column(db.String(50))
    apellido_paterno = db.Column(db.String(50))
    apellido_materno = db.Column(db.String(50))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(50))

    def __init__(self, clienteid, dni, nombre, apellido_paterno, apellido_materno, telefono, direccion):
        self.clienteid = clienteid
        self.dni = dni
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.telefono = telefono
        self.direccion = direccion

    def serialize(self):
        return {
            'clienteid': self.clienteid,
            'dni': self.dni,
            'nombre': self.nombre,
            'apellido_paterno': self.apellido_paterno,
            'apellido_materno': self.apellido_materno,
            'telefono': self.telefono,
            'direccion': self.direccion
        }
