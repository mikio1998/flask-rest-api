from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import helper

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
# products_path = "./data/products.csv"
products_path = "./data/helikon.csv"

# /sold
sold_products_path = "./data/sold.csv"

# /barcode
barcode_path = "./data/barcode.csv"

class ProductsList(Resource):
    def get(self, vendor):        
        data = pd.read_csv(products_path, keep_default_na=False)
        data = helper.decode_products_data(data, vendor)
            
        return {"data": data}, 200

# Sold Products backend handled with Firestore.
class SoldProductsList(Resource):
    def get(self):
        data = pd.read_csv(sold_products_path, keep_default_na=False)
        data = helper.decode_sold_products_data(data)
        return {"data": data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("handle", required=True, type=str)
        parser.add_argument("name", required=True, type=str)
        parser.add_argument("vendor", required=True, type=str)
        parser.add_argument("price", required=True, type=str)
        parser.add_argument("size", required=True, type=str)
        parser.add_argument("color", required=True, type=str)
        parser.add_argument("url", required=True, type=str)
        parser.add_argument("quantity", required=True, type=int)
        args = parser.parse_args()
        data = pd.read_csv(sold_products_path)
        
        data = data.append({
            "Handle": args["handle"],
            "Title": args["name"],
            "Vendor": args["vendor"],
            "Option1 Name": "Color",
            "Option1 Value": args["color"],
            "Option2 Name": "Size",
            "Option2 Value": args["size"],
            "Variant Price": args["price"],
            "Variant Image": args["url"],
            "Quantity": args["quantity"]
        }, ignore_index=True)
        data.to_csv(sold_products_path, index=False) # save it to csv
        return {"data": helper.decode_sold_products_data(data)}, 200 #dataframe to dict
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("handle", required=True, type=str)
        parser.add_argument("size", required=True, type=str)
        parser.add_argument("color", required=True, type=str)
        args = parser.parse_args()
        
        data = pd.read_csv(sold_products_path)
        
        # Find t
        
        if args["handle"] in list(data["Handle"]):
            
            # select the rows that aren't equal to the handle specified
            data = data[data["userId"] != str(args["userId"])]
            
            #
            data.to_csv(users_path, index=False)
            return {"data": data.to_dict()}, 200
        else: # User doesn't exist
            return {"message": f"{args['userId']} does not exist."}, 404
        
        
class Product(Resource):
    def get(self, handle):
        data = pd.read_csv(products_path, keep_default_na=False)
        
        # Find product
        for index, row in data.iterrows():
            if row["Handle"] == handle:
                obj = helper.row_to_object(row)
                return obj, 200
        return {
                "message": f"{handle} does not exists."
            }, 409 #req conflict 
    
class Barcode(Resource):
    def get(self, barcode):
        # parser = reqparse.RequestParser()
        # parser.add_argument("barcode", required=True, type=str)
        # args = parser.parse_args()
        
        data = pd.read_csv(barcode_path)
        
        # Find the handle for the barcode.
        handle = None
        for index, row in data.iterrows():
            if row["Barcode"] == barcode:
                handle = row["Product Handle"]
                break 

        if handle == None:
            return {
                "message": f"{barcode} does not exists."
            }, 409 #req conflict  
        
        # Next, match the handle with a product.
        prodData = pd.read_csv(products_path)
        res = helper.get_variants(prodData, handle)
        if len(res[handle]) == 0:
            return {
                "message": f"{barcode} does not exists."
            }, 409 #req conflict  
        else:
            return {"data": res}, 200


# Map Resource classes, to addresses /
api.add_resource(ProductsList, "/productslist/<vendor>")
api.add_resource(Product, "/product/<handle>")
api.add_resource(SoldProductsList, "/soldproducts")
api.add_resource(Barcode, "/barcode/<barcode>")

if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
# class Users(Resource):
#     def get(self):
#         data = pd.read_csv(users_path)
#         data = data.to_dict()
        
#         return {"data": data}, 200
    
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument("userId", required=True, type=int)
#         parser.add_argument("name", required=True, type=str)
#         parser.add_argument("city", required=True, type=str)
#         args = parser.parse_args()
        
#         # Check if user id already exists
#         data = pd.read_csv(users_path)
#         if args["userId"] in data["userId"]:
#             return {
#                 "message": f"{args['userId']} already exists."
#             }, 409 #req conflict
#         else:
#             data = data.append({
#                 "userId": args["userId"],
#                 "name": args["name"],
#                 "city": args["city"],
#                 "locations": []
#             }, ignore_index = True)
#             data.to_csv(users_path, index=False) # save it to csv
#             return {"data": data.to_dict()}, 200 # dataframe to dict
        
#     def delete(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument("userId", required=True, type=int)
#         args = parser.parse_args()
        
#         data = pd.read_csv(users_path)
        
#         if args["userId"] in list(data["userId"]):
#             # select the rows that aren't equal to the userId specified
#             data = data[data["userId"] != str(args["userId"])]
#             data.to_csv(users_path, index=False)
#             return {"data": data.to_dict()}, 200
#         else: # User doesn't exist
#             return {"message": f"{args['userId']} does not exist."}, 404

# class Locations(Resource):
#     #get
#     def get(self):
#         # data = pd.read_csv(locations_path)
#         data = pd.read_csv(helikon_path)
#         # data = data.to_dict()
#         data = data_to_dict(data)
#         return {"data": data}, 200
    
#     #post
#     def post(self):
#         # parse args
#         parser = reqparse.RequestParser()
#         parser.add_argument("locationId", required=True, type=int)
#         parser.add_argument("name", required=True, type=str)
#         parser.add_argument("rating", required=True, type=float)
#         args = parser.parse_args()
        
#         # Check if location id already exists
#         data = pd.read_csv(locations_path)
#         if args["locationId"] in data["locationId"]:
#             return {
#                 "message": f"{args['locationId']} already exists."
#         }, 409 # req conflict
#         else:
#             data = data.append({
#                 "locationId": args["locationId"],
#                 "name": args["name"],
#                 "rating": args["rating"]
#             }, ignore_index=True)
#             data.to_csv(locations_path, index=False) # save it to csv
#             return {"data": data.to_dict()}, 200 #dataframe to dict
            
        
# api.add_resource(Users, "/users")
# api.add_resource(Locations, "/locations")