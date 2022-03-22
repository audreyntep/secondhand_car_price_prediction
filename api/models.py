from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class Estimations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), unique=False, nullable=False)
    fuel_id = db.Column(db.Integer, db.ForeignKey('fuels.id'), unique=False, nullable=False)
    gearbox_id = db.Column(db.Integer, db.ForeignKey('gearboxes.id'), unique=False, nullable=False) 
    year = db.Column(db.String(150))
    kilometers = db.Column(db.Integer)
    seat = db.Column(db.Integer)
    door = db.Column(db.Integer)
    estimation = db.Column(db.Integer)
    co2 = db.Column(db.Integer)
    location = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

class Brands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    estimation =  db.relationship('Estimations')
    #models =  db.relationship('Models')

class Models(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    #estimation =  db.relationship('Estimations')
    #brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), unique=False, nullable=False) 

class Fuels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    estimation =  db.relationship('Estimations')

class Gearboxes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    estimation =  db.relationship('Estimations')

class Doors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, unique=True, nullable=False)

class Seats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, unique=True, nullable=False)

class Pollutions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, unique=True, nullable=False)

