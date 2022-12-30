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

# /helikon
helikon_path = "./data/helikon.csv"

# /products
products_path = "./data/products.csv"

def data_to_dict(df, vendor):
    dict = {}
    
    for index, row in df.iterrows():
        if row["Vendor"] != vendor:
            continue
        
        color = None
        if row["Option1 Name"] == "Color":
            color = row["Option1 Value"]
        elif row["Option2 Name"] == "Color":
            color = row["Option2 Value"]
            
        size = None
        if row["Option1 Name"] == "Size":
            size = row["Option1 Value"]
        elif row["Option2 Name"] == "Size":
            size = row["Option2 Value"]
            
        url = row["Variant Image"]
        if url == "":
            url = None
        
        # If id exists
        if row["Handle"] in dict:
            dict[row["Handle"]]["variants"] += [{
                    "name": dict[row["Handle"]]["name"],
                    "vendor": dict[row["Handle"]]["vendor"],
                    "price": dict[row["Handle"]]["price"],
                    "size": size,
                    "color": color,
                    "url": url
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
                    "size": size,
                    "color": color,
                    "url": url
                }]}
    return dict

class Products(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("vendor", required=True, type=str)
        args = parser.parse_args()
        
        data = pd.read_csv(products_path, keep_default_na=False)
        data = data_to_dict(data, args["vendor"])
            
        return {"data": data}, 200





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
        # data = pd.read_csv(locations_path)
        data = pd.read_csv(helikon_path)
        # data = data.to_dict()
        data = data_to_dict(data)
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
api.add_resource(Products, "/products")




if __name__ == "__main__":
    app.run(debug=True)
    