from utils.db import db

class DetalleOrden(db.Model):
    __tablename__ = 'detalle_orden'
    
    detalleid = db.Column(db.Integer, primary_key=True)
    ordencompraid = db.Column(db.Integer)
    libroid = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    precio_unitario = db.Column(db.Integer)
    
    
    
    def __init__(self, ordencompraid, libroid, cantidad, precio_unitario):
        self.ordencompraid = ordencompraid
        self.libroid = libroid
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def serialize(self):
        return {
            'detalleid': self.detalleid,
            'ordencompraid': self.ordencompraid,
            'libroid': self.libroid,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario
        }