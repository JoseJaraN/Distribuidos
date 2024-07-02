from utils.db import db


class Libro(db.Model):
    __tablename__ = 'libro'
    libroid = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    descripción = db.Column(db.String(100))

    def __init__(self, libroid, nombre, precio, cantidad, descripción):
        self.libroid = libroid
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.descripcion = descripción

    def serialize(self):
        return {
            'libroid': self.libroid,
            'nombre': self.nombre,
            'precio': self.precio,
            'cantidad': self.cantidad,
            'descripción': self.descripción
        }