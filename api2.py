from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

# Initialize our flask app, init flask api.
app = Flask(__name__)
api = Api(app)

# Endpoints
# /users
# /locations

class Users(Resource):
	pass

class Locations(Resource):
	pass

# Map class Users, to address /users
api.add_resource(Users, "/users")
api.add_resource(Locations, "/locations")


if __name__ == "__main__":
	app.run()