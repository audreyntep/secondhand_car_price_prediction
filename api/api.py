import json
from flask_restful import reqparse, abort, Resource
from .models import db, Estimations, Brands, Fuels, Gearboxes, Pollutions, Doors, Seats
from model_audrey import get_data_from_csv, get_decision_tree_rfe
from model_anouar import get_random_forest, scale_data
import pandas as pd


# Ajout des paramètres URL
parser = reqparse.RequestParser()
parser.add_argument('brand')
parser.add_argument('year')
parser.add_argument('fuel')
parser.add_argument('gearbox')
parser.add_argument('kilometers')
parser.add_argument('location')
parser.add_argument('co2')
parser.add_argument('door')
parser.add_argument('seat')
parser.add_argument('id')
parser.add_argument('prediction')


# interrompt l'action si l'id d'estimation n'existe pas dans la BDD
def abort_if_id_doesnt_exist(id):
    if Estimations.query.get(id) is None:
        abort(404, message="Estimation {} doesn't exist".format(id))

# retourne un dictionnaire de critères {id:name}
def get_criterias_from_BDD(Object):
    criterias = {}
    for i in Object:
        criterias[i.id] = i.name
    return criterias

# retourne une prédiction
def get_prediction_from_model(data, model):
    print(data)
    if model == 'decision tree':
        prediction = get_decision_tree_rfe().predict(data)
        for p in prediction:
            return p
    if model == 'random forest':
        prediction = get_random_forest().predict(data)
        for p in prediction:
            return p

# retourne un dictionnaire de predictions
def get_estimations_from_BDD(Estimation):
    estimations = {}
    print(Estimation)
    for i in Estimation:
        estimations[i.id] = {
            'brand':Brands.query.filter_by(id=i.brand_id).first().name,
            'fuel':Fuels.query.filter_by(id=i.fuel_id).first().name,
            'gearbox':Gearboxes.query.filter_by(id=i.gearbox_id).first().name,
            'year':i.year,
            'kilometers':i.kilometers,
            'door':i.door,
            'seat':i.seat,
            'co2':i.co2,
            'location':i.location,
            'estimation':i.estimation,
            'created_at':"{}-{}-{}".format(i.created_at.year,i.created_at.month,i.created_at.day)
            }
    return estimations


# GET to Home
class Home(Resource):
    def get(self):
        #return model_audrey.get_data_from_csv()
        return "Welcome on Autoccaz Api"


# GET to show a list of all criterias, and POST to add a new value
class Criterias(Resource):

    # retourne les critères depuis la BDD
    def get(self):
        criterias = {}
        criterias['brands'] = get_criterias_from_BDD(Brands.query.all())
        criterias['fuels'] = get_criterias_from_BDD(Fuels.query.all())
        criterias['gearboxes'] = get_criterias_from_BDD(Gearboxes.query.all())
        criterias['pollutions'] = get_criterias_from_BDD(Pollutions.query.all())
        criterias['doors'] = get_criterias_from_BDD(Doors.query.all())
        criterias['seats'] = get_criterias_from_BDD(Seats.query.all())
        return criterias

    # insérer des catégories de variables dans la BDD depuis le csv
    def post(self):
        criterias = get_data_from_csv()
        # insertion des catégories des variables dans les tables
        if criterias != None:
            print(criterias)
            for key in criterias:
                if key == 'Marque':
                    for brand in criterias[key]:
                        db.session.add(Brands(name=criterias[key][brand]))
                if key == 'Carburant':
                    for fuel in criterias[key]:
                        db.session.add(Fuels(name=criterias[key][fuel]))
                if key == 'Emission Co2':
                    for co2 in criterias[key]:
                        db.session.add(Pollutions(name=criterias[key][co2]))
                if key == 'Transmission':
                    for gearbox in criterias[key]:
                        db.session.add(Gearboxes(name=criterias[key][gearbox]))
                if key == 'nbPlace':
                    for seat in criterias[key]:
                        db.session.add(Seats(name=criterias[key][seat]))
                if key == 'nbPortes':
                    for door in criterias[key]:
                        db.session.add(Doors(name=criterias[key][door]))
                db.session.flush()
                db.session.commit()
            return 204
        

# GET retourne la liste des valeurs pour une critère
class Criteria(Resource):
    
    # retourne un critère
    def get(self, critere):
        if critere == 'brand':
            return get_criterias_from_BDD(Brands.query.all())
        if critere == 'fuel':
            return get_criterias_from_BDD(Fuels.query.all())
        if critere == 'gearbox':
            return get_criterias_from_BDD(Gearboxes.query.all())
        if critere == 'pollution':
            return get_criterias_from_BDD(Pollutions.query.all())
        if critere == 'door':
            return get_criterias_from_BDD(Doors.query.all())
        if critere == 'seat':
            return get_criterias_from_BDD(Seats.query.all())


# GET retourne une prédiction, DELETE pour supprimer une prédiction
class Prediction(Resource):

    # retourne l'estimation de l'id renseigné
    def get(self, id):
        abort_if_id_doesnt_exist(id)
        estimation = Estimations.query.get(id)
        return {
            'brand':Brands.query.filter_by(id=estimation.brand_id).first().name,
            'fuel':Fuels.query.filter_by(id=estimation.fuel_id).first().name,
            'gearbox':Gearboxes.query.filter_by(id=estimation.gearbox_id).first().name,
            'year':estimation.year,
            'kilometers':estimation.kilometers,
            'door':estimation.door,
            'seat':estimation.seat,
            'location':estimation.location,
            'co2': estimation.co2,
            'estimation':estimation.estimation,
            'created_at':"{}-{}-{}".format(estimation.created_at.year,estimation.created_at.month,estimation.created_at.day)
        }
    # supprimer l'estimation de l'id
    def delete(self, id):
        abort_if_id_doesnt_exist(id)
        db.session.delete(Estimations.query.get(id))
        db.session.commit()
        return '', 204


# ARBRE DE DECISION
# GET to show a list of all estimations, and POST to add a new estimation
class DecisionTree(Resource):
    # retourne la liste des estimations
    def get(self):
        return get_estimations_from_BDD(Estimations.query.all())

    # insert une estimation
    def post(self):
        # récupération des arguments
        args = parser.parse_args()
        print(args)
        year=int(args['year'])
        kilometers=int(args['kilometers'])
        door = Doors.query.filter_by(id=int(args['door'])).first().name
        seat = Seats.query.filter_by(id=int(args['seat'])).first().name
        co2 = Pollutions.query.filter_by(id=int(args['co2'])).first().name

        # importation du modèle, calcul de la prediction
        X = pd.DataFrame(data=[[year, door, seat, kilometers]], columns=['Année','nbPortes','nbPlace','Kilométrage'])
        prediction = round(get_prediction_from_model(X, 'decision tree'))
        print(prediction)

        # insertion de la prediction dans la BDD
        if args['brand'] != '':
            estimation = Estimations(
                brand_id=args['brand'],
                fuel_id=args['fuel'],
                gearbox_id=args['gearbox'],
                year=year,
                kilometers=kilometers,
                door=door,
                seat=seat,
                co2=co2,
                location=int(args['location']),
                estimation=prediction)
            db.session.add(estimation)
            db.session.commit()

        return estimation.id



# MODEL RANDOM FOREST
Marques = {
    'BMW':0,
    'RENAULT':1,
    'PEUGEOT':2,
    'VOLKSWAGEN':3,
    'AUDI':4,
}
Carburants = {
    'Diesel':0,
    'Essence':1,
    'Electric':2,
}
Transmissions = {
    'Manuelle':0,
    'Automatique':1,
}



# GET to show a list of all estimations, and POST to add a new estimation
class RandomForest(Resource):
    # retourne la liste des estimations
    def get(self):
        #return get_estimations_from_BDD(Estimations.query.all())
        return json.dumps([Marques, Carburants,Transmissions])

    # insert une estimation
    def post(self):
        # récupération des arguments
        args = parser.parse_args()
        print(args)
        brand = Marques.get(args['brand'])
        year=int(args['year'])
        fuel=Carburants.get(args['fuel'])
        zipcode=int(args['location'])
        km=int(args['kilometers'])
        gearbox = Transmissions.get(args['gearbox'])
        
        # importation du modèle, calcul de la prediction
        X = pd.DataFrame(data=[[brand, year ,fuel, zipcode, km]], columns=['Marque','Année','Carburant','CodePostal','Kilométrage'])
        print(X)
        prediction = round(get_prediction_from_model(scale_data(X), 'random forest'))
        print(prediction)
        return prediction
