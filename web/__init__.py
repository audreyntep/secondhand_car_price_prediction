from flask import Flask, Blueprint, redirect, render_template, request, url_for
import requests
import os
import urllib.parse

views = Blueprint('views', __name__)

def create_app():
    app = Flask('web')
    app.debug = True

    print('web', app.config)

    # Define route with Blueprint
    app.register_blueprint(views, url_prefix='/')
    
    return app

@views.route('/', methods=['GET'])
def home():
    #o = urllib.parse.urlparse('http://localhost:5000/api')
    #print(o.scheme)
    return render_template("home.html")

@views.route('/test')
def test():

    return '<p>teste</p>'



