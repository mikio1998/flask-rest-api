from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

# Initialize our flask app, init flask api.
app = Flask(__name__)
api = Api(app)

# Endpoints

# /users
users_path = "./data/users.csv"

# /locations
locations_path = "./data/locations.csv"

class Users(Resource):
    def get(self):
        data = pd.read_csv(users_path)
        data = data.to_dict()
        return {"data": data}, 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("locationId", required=True, type=int)
        parser.add_argument("name", required=True, type=str)
        parser.add_argument("city", required=True, type=str)
        args = parser.parse_args()
        return {
            "loc": args["locationId"],
            "name": args["name"],
            "city": args["city"]
        }, 200

class Locations(Resource):
    pass

# Map class Users, to address /users
api.add_resource(Users, "/users")
api.add_resource(Locations, "/locations")


if __name__ == "__main__":
    app.run(debug=True)