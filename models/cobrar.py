from utils.db import db

class Cobrar(db.Model):
    __tablename__ = 'cobrar'
    cobrarid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clienteid = db.Column(db.Integer)
    ordencompraid = db.Column(db.Integer)
    preciototal = db.Column(db.Integer)

  
    def __init__(self, clienteid, ordencompraid, preciototal):
        self.clienteid = clienteid
        self.ordencompraid = ordencompraid
        self.preciototal = preciototal

 
    def serialize(self):
        return {
            'cobrarid': self.cobrarid,
            'clienteid': self.clienteid,
            'ordencompraid': self.ordencompraid,
            'preciototal': self.preciototal
        }