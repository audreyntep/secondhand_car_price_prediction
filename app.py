from flask import Flask, render_template
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
import os


current_directory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.testing = True

@app.route('/')
def home():
    pred = {'pred':2000}
    return render_template("prediction.html", pred=pred)

db = SQLAlchemy('app')

if __name__ == '__main__':
    app.run(debug=True)

