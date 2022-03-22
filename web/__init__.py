from re import U
from flask import Flask, Blueprint, render_template, request
import requests

from api.models import Brands

views = Blueprint('views', __name__)

def create_app():
    app = Flask('web')

    # Config flask app
    app.debug = True
    #print('web', app.config)

    # Define route with Blueprint
    app.register_blueprint(views, url_prefix='/')

    return app

@views.route('/', methods=['GET','POST'])
def home():
    url = 'http://127.0.0.1:5000/'

    prediction = None
    criterias = requests.get(url=url+'criteres').json()
    #print('critères :', criterias)

    if request.method  == 'POST':
        # récupération des paramètres URL et envoi d'une requête de prédiction à l'api
        r = requests.post(
            url=url+'prediction', 
            data = {
                'brand':request.form.get('brand'),
                'year': request.form.get('year'),
                'fuel':request.form.get('fuel'),
                'gearbox': request.form.get('gearbox'),
                'kilometers':request.form.get('kilometers'),
                'location':request.form.get('location'),
                'co2': request.form.get('co2'),
                'door': request.form.get('door'),
                'seat': request.form.get('seat')
            })
        print(r.text)
        prediction = requests.get(url=url+'prediction/'+r.text).json()
        print(prediction)
        return render_template("home.html", results=criterias, prediction=prediction)

    return render_template("home.html", results=criterias, prediction=prediction)



