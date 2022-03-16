from flask import Blueprint, render_template
import requests
from os import path

views = Blueprint('views', __name__)

@views.route('/')
def home():
    SITE_NAME = 'http://localhost:5000/api/criteres'
    print(requests.options(SITE_NAME))
    #print(requests.get(f'{SITE_NAME}{path}'))
    return render_template("home.html")

