import json
import os
import datetime
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask import Flask, request, jsonify, send_file
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from model import Model

with open("config.json") as jsondata:
    config = json.load(jsondata)

app = Flask(__name__)
app.config[
    "MONGO_URI"
] = f'mongodb+srv://{config["USER"]}:{config["PASS"]}@cluster0.xsrdmeh.mongodb.net/{config["DB"]}?retryWrites=true&w=majority'
app.config["SLIDER_IMAGES"] = f"SliderImages\\"
cors = CORS(app)
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
            return jsonify({"status": True, "message": "Creds updated successfully"})
        else:
            return jsonify({"status": False, "error": "[DB-ERROR]:Creds update failed"})

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
            return jsonify({"status": False, "error": "[DB-ERROR]:Info update failed"})

    def get(self):
        contact_info = model.get_contact_info()
        return jsonify(
            {"telephone": contact_info["telephone"], "mail": contact_info["mail"]}
        )


@api.route("/slider_pic")
class SliderPic(Resource):
    def post(self):
        split_filename = os.path.splitext(request.files["sliderPic"].filename)
        file_extension = split_filename[len(split_filename) - 1]
        print(split_filename, file_extension)
        if [".png", ".jpeg", ".jpg"].count(file_extension) == 0:
            return jsonify({"status": False, "error": "[EXT-ERROR]:File type invalid"})
        request.files["sliderPic"].filename = (
            str(datetime.datetime.now()) + request.files["sliderPic"].filename
        )
        img = f'{ app.config["SLIDER_IMAGES"]+secure_filename(request.files["sliderPic"].filename)}'
        inserted_id = model.add_slider_image({"path": img})
        if inserted_id is None:
            return jsonify({"status": False, "error": "[DB-ERROR]:Image upload failed"})
        request.files["sliderPic"].save(
            app.config["SLIDER_IMAGES"]
            + secure_filename(request.files["sliderPic"].filename)
        )
        return jsonify(
            {
                "status": True,
                "message": "Image uploaded successfully",
            }
        )

    def get(self):
        if request.args.get("id") == "all":
            pics = model.get_all_pics()
            return jsonify({"payload": pics})
        else:
            os.remove(request.args.get("path"))
            return jsonify({"status": model.remove_pic(request.args.get("id"))})


@api.route("/slider_pic_display")
class SliderPicDisplay(Resource):
    def get(self):
        return send_file(request.args.get("path"))


if __name__ == "__main__":
    app.run(debug=True)
