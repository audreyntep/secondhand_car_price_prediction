from flask import Flask
from flask_restful import Api
from .models import db
from .api import Predictions, Prediction, Criterias, Criteria, Home
from os import path


def create_app():
    app = Flask('api')

    # Config flask app
    app.debug = True
    app.config['SECRET_KEY'] = 'test'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    #print('api',app.config)

    # Initialise and create BDD
    db.init_app(app)
    create_database(app)

    api = Api(app)
    # Define route with Resource
    api.add_resource(Predictions, '/prediction')
    api.add_resource(Prediction, '/prediction/<id>')
    api.add_resource(Criterias, '/criteres')
    api.add_resource(Criteria, '/<critere>')
    api.add_resource(Home, '/')
    
    return app

# créer la BDD si le fichier .db n'exsite pas
def create_database(my_app):
    if not path.exists('app/database.db'):
        # creation des tables dans la BDD
        db.create_all(app=my_app)
        print('Database created!')
