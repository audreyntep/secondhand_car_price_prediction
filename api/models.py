from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class Estimations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marque = db.Column(db.String(150))
    model = db.Column(db.String(150))
    year = db.Column(db.String(150))
    fuel = db.Column(db.String(150))
    location = db.Column(db.String(150))
    kilometers = db.Column(db.Integer)
    gear_box = db.Column(db.String(150))
    estimation = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

class Brands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    models =  db.relationship('Models')

class Models(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), unique=False, nullable=False) 

class Fuels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

class Gearboxes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

