from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from os import path
from .models import db, Estimations, Brands, Models, Fuels, Gearboxes


def create_app():
    app = Flask('api')

    app.debug = True
    app.config['SECRET_KEY'] = 'test'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    create_database(app)

    api = Api(app)
    # Define route with Resource
    api.add_resource(Predictions, '/prediction')
    api.add_resource(Criterias, '/criteres')

    print('api',app.config)
    return app

# Ajout des paramètres URL
parser = reqparse.RequestParser()
parser.add_argument('brand')
parser.add_argument('model')
parser.add_argument('year')
parser.add_argument('fuel')
parser.add_argument('gear_box')
parser.add_argument('kilometers')
parser.add_argument('location')
parser.add_argument('id')


TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

# Todo
# shows a single todo item and lets you delete a todo item
class Brand(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self):
        print('put')
        args = parser.parse_args()
        #task = {'task': args['task']}
        #TODOS[todo_id] = task
        #return task, 201
        marque = args['marque']
        db.session.add(Brands(name=marque))
        db.session.commit()
        return 201


# List
# GET to show a list of all estimations, and POST to add a new estimation
class Predictions(Resource):

    def get(self):
        return Estimations.query.all()

    def post(self):
        args = parser.parse_args()
        #todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        #todo_id = 'todo%i' % todo_id
        #TODOS[todo_id] = {'task': args['task']}
        #return TODOS[todo_id], 201
        marque = args['marque']
        print(args)
        db.session.add(Brands(name=marque))
        db.session.commit()
        return 201

# Criterias
# GET to show a list of all criterias, and POST to add a new value
class Criterias(Resource):
    def get(self):
        criterias = {}
        criterias['brands'] = get_criterias(Brands.query.all())
        criterias['models'] = get_criterias(Models.query.all())
        criterias['fuels'] = get_criterias(Fuels.query.all())
        criterias['gearboxes'] = get_criterias(Gearboxes.query.all())
        return criterias
    
    def post(self):
        args = parser.parse_args()
        if args['brand'] and args['model'] is None:
            db.session.add(Brands(name=args['brand']))
        if args['model']:
            id = Brands.query.filter_by(name=args['brand']).first()
            db.session.add(Models(name=args['model'], brand_id=id.id))
        if args['fuel']:
            db.session.add(Fuels(name=args['fuel']))
        if args['gear_box']:
            db.session.add(Gearboxes(name=args['gear_box']))
        db.session.commit()
        return args, 201



# Create database if not exists
def create_database(app):
    if not path.exists('app/database.db'):
        db.create_all(app=app)
        print('Database created!')

# Format list result into dictionnary for criterias
def get_criterias(Object):
    criterias = {}
    for i in Object:
        criterias[i.id] = i.name
    return criterias

