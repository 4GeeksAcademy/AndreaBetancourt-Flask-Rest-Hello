"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets # Editar para agregar nuevos modelos cada que se crea en admin y models
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



# Endpoints: Aqui inicia el codigo


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets ():
    planets = Planets.query.all() #query.all trae todo lo que esta dentro de Planets en una lista
    planets_serialized = [planet.serialize() for planet in planets]
    return jsonify(planets_serialized)


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planets_id (planet_id):
    planet = Planets.query.filter_by(id = planet_id)
    planet_serialized_id = [planet[0].serialize()]
    return jsonify(planet_serialized_id)


@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    people_serialized = [person.serialize() for person in people]
    return jsonify(people_serialized)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
