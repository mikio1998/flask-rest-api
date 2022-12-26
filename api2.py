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
        parser.add_argument("userId", required=True, type=int)
        parser.add_argument("name", required=True, type=str)
        parser.add_argument("city", required=True, type=str)
        args = parser.parse_args()
        
        # Check if user id already exists
        data = pd.read_csv(users_path)
        if args["userId"] in data["userId"]:
            return {
                "message": f"{args['userId']} already exists."
            }, 409 #req conflict
        else:
            data = data.append({
                "userId": args["userId"],
                "name": args["name"],
                "city": args["city"],
                "locations": []
            }, ignore_index = True)
            data.to_csv(users_path, index=False) # save it to csv
            return {"data": data.to_dict()}, 200 # dataframe to dict
        
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userId", required=True, type=int)
        args = parser.parse_args()
        
        data = pd.read_csv(users_path)
        
        if args["userId"] in data["userId"]:
            # select the rows that aren't equal to the userId specified
            data = data[data["userId"] != str(args["userId"])]
            data.to_csv(users_path, index=False)
            return {"data": data.to_dict()}, 200
        else: # User doesn't exist
            return {"message": f"{args['userId']} does not exist."}, 404

class Locations(Resource):
    pass

# Map class Users, to address /users
api.add_resource(Users, "/users")
api.add_resource(Locations, "/locations")


if __name__ == "__main__":
    app.run(debug=True)
    