import json
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from model import Model

with open("config.json") as jsondata:
    config = json.load(jsondata)

app = Flask(__name__)
app.config[
    "MONGO_URI"
] = f'mongodb+srv://{config["USER"]}:{config["PASS"]}@cluster0.xsrdmeh.mongodb.net/{config["DB"]}?retryWrites=true&w=majority'
cors = CORS(app)
app.config["SECRET_KEY"] = "your-secret-key"
api = Api(app)
mongo = PyMongo(app)
model = Model()
model.mongo = mongo.db
model.initialize_collections()


@api.route("/admin_info")
class AdminInfo(Resource):
    def post(self):
        admin_info = {
            "username": request.json["username"],
            "password": request.json["password"],
        }
        if model.update_admin_info(admin_info):
            return jsonify(
                {"status": True, "message": "Admin info updated successfully"}
            )
        else:
            return jsonify({"status": False, "error": "Admin info updation failed"})

    def get(self):
        admin_info = model.get_admin_info()
        return jsonify(
            {"username": admin_info["username"], "password": admin_info["password"]}
        )


@api.route("/contact_info")
class ContactInfo(Resource):
    def post(self):
        contact_info = {
            "telephone": request.json["telephone"],
            "mail": request.json["mail"],
        }
        if model.update_contact_info(contact_info):
            return jsonify(
                {"status": True, "message": "Contact info updated successfully"}
            )
        else:
            return jsonify({"status": False, "error": "Contact info updation failed"})

    def get(self):
        contact_info = model.get_contact_info()
        return jsonify(
            {"telephone": contact_info["telephone"], "mail": contact_info["mail"]}
        )


if __name__ == "__main__":
    app.run(debug=True)
