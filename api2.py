from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
#import untitled0

# Initialize our flask app, init flask api.
app = Flask(__name__)
api = Api(app)

# Endpoints

# /users
users_path = "./data/users.csv"

# /locations
locations_path = "./data/locations.csv"

# /helikon
helikon_path = "./data/helikon.csv"

#TODOS: create paths for csvs, make path a parameter.
    

def data_to_dict(df):
    dict = {}
    
    for index, row in df.iterrows():
        # If id exists
        if row["Handle"] in dict:
            dict[row["Handle"]]["variants"] += [{
                    "name": dict[row["Handle"]]["name"],
                    "vendor": dict[row["Handle"]]["vendor"],
                    "price": dict[row["Handle"]]["price"],
                    "size": row["Option2 Value"],
                    "color": row["Option1 Value"],
                    "url": row["Variant Image"]
                }]
        else:
            dict[row["Handle"]] = {
                "name": row["Title"],
                "vendor": row["Vendor"],
                "price": row["Variant Price"],
                "variants": [{
                    "name": row["Title"],
                    "vendor": row["Vendor"],
                    "price": row["Variant Price"],
                    "size": row["Option2 Value"],
                    "color": row["Option1 Value"],
                    "url": row["Variant Image"]
                }]}
    return dict

class Products(Resource):
    def get(self):
        # arg for path
        parser = reqparse.RequestParser()
        parser.add_argument("vendor", required=True, type=str)
        args = parser.parse_args()
        
        path = ""
        
        if args["vendor"] == "helikon":
            path = helikon_path
        else:
            return {
                "message": f"{args['vendor']} does not exist."
                }, 409 #req conflict
        
        data = pd.read_csv(path)
        #data = data.to_dict()
        data = data_to_dict(data)
            
        return {"data": data}, 200





class Users(Resource):
    def get(self):
        #data = pd.read_csv(untitled0.users_path)
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
        
        if args["userId"] in list(data["userId"]):
            # select the rows that aren't equal to the userId specified
            data = data[data["userId"] != str(args["userId"])]
            data.to_csv(users_path, index=False)
            return {"data": data.to_dict()}, 200
        else: # User doesn't exist
            return {"message": f"{args['userId']} does not exist."}, 404

class Locations(Resource):
    #get
    def get(self):
        data = pd.read_csv(locations_path)
        data = data.to_dict()
        return {"data": data}, 200
    
    #post
    def post(self):
        # parse args
        parser = reqparse.RequestParser()
        parser.add_argument("locationId", required=True, type=int)
        parser.add_argument("name", required=True, type=str)
        parser.add_argument("rating", required=True, type=float)
        args = parser.parse_args()
        
        # Check if location id already exists
        data = pd.read_csv(locations_path)
        if args["locationId"] in data["locationId"]:
            return {
                "message": f"{args['locationId']} already exists."
        }, 409 # req conflict
        else:
            data = data.append({
                "locationId": args["locationId"],
                "name": args["name"],
                "rating": args["rating"]
            }, ignore_index=True)
            data.to_csv(locations_path, index=False) # save it to csv
            return {"data": data.to_dict()}, 200 #dataframe to dict
            
        
        

# Map class Users, to address /users
api.add_resource(Users, "/users")
api.add_resource(Locations, "/locations")
api.add_resource(Products, "/helikon")




if __name__ == "__main__":
    app.run(debug=True)
    