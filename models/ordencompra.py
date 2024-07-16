from utils.db import db


class OrdenCompra(db.Model):
    __tablename__ = 'ordencompra'
    
    ordencompraid = db.Column(db.Integer, primary_key=True)
    clienteid = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    preciototal = db.Column(db.Integer)
    horapago = db.Column(db.Time)
    
    
    def __init__(self, clienteid, fecha, preciototal, horapago):
        self.clienteid = clienteid
        self.fecha = fecha
        self.preciototal = preciototal
        self.horapago = horapago

    def serialize(self):
        return {
            'ordencompraid': self.ordencompraid,
            'clienteid': self.clienteid,
            'fecha': self.fecha.isoformat(),  # Formato ISO 8601 para fecha
            'preciototal': self.preciototal,
            'horapago': self.horapago.strftime('%H:%M:%S')  # Formato de hora
        }
