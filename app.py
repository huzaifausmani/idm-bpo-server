import json
import os
import datetime
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask import Flask, request, jsonify, send_file
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from model import Model
from smtp import send_email

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
    
@api.route("/validate_login")
class Validatelogin(Resource):
    def post(self):
        admin_info = model.get_admin_info()
        if (request.json["username"] == admin_info["username"] and request.json["password"] == admin_info["password"]):
            return jsonify({"status": True, "message": "⚠ Login successfully"})
        else:
            return jsonify({"status": False, "error": "⚠ Creds not valid"})
        
@api.route("/forget_credentials")
class ForgetCredentials(Resource):
    def get(self):
        admin_info = model.get_admin_info()
        # code for smtp
        flag = send_email(admin_info["username"], admin_info["password"])
        if (flag):
            return jsonify({"status": True, "message": "Credentials has been sent successfully!"})
        else:
            return jsonify({"status": False, "message": "There was an error in sending credentials!"})
       
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
            return jsonify(
                {
                    "status": model.remove_pic(request.args.get("id")),
                    "message": "Image removed successfully",
                }
            )


@api.route("/slider_pic_display")
class SliderPicDisplay(Resource):
    def get(self):
        return send_file(request.args.get("path"))


@api.route("/comments")
class Comments(Resource):
    def post(self):
        comment = {
            "commenter_name": request.json["commenter_name"],
            "comment_text": request.json["comment_text"],
            "service_option": request.json["service_option"],
            "rating": request.json["rating"],
        }
        if model.add_comment(comment):
            return jsonify({"status": True, "message": "Commented posted successfully"})
        else:
            return jsonify(
                {"status": False, "error": "[DB-ERROR]:Comment posting failed"}
            )

    def get(self):
        id = request.args.get("id")
        if id is None:
            return jsonify({"payload": model.get_all_comments()})
        else:
            return jsonify(
                {
                    "status": model.remove_comment(id),
                    "message": "Comment removed successfully",
                }
            )


@api.route("/services")
class Services(Resource):
    def post(self):
        service = {"service_name": request.json["service_name"]}
        if model.add_service(service):
            return jsonify({"status": True, "message": "Service added successfully"})
        else:
            return jsonify(
                {"status": False, "error": "[DB-ERROR]:Service adding failed"}
            )

    def get(self):
        id = request.args.get("id")
        if id is None:
            return jsonify({"payload": model.get_all_services()})
        else:
            return jsonify(
                {
                    "status": model.remove_service(id),
                    "message": "Service removed successfully",
                }
            )


@api.route("/requests")
class Requests(Resource):
    def post(self):
        _request = {
            "request_category": request.json["request_category"],
            "requestee_name": request.json["requestee_name"],
            "requestee_email": request.json["requestee_email"],
            "requestee_company": request.json["requestee_company"],
            "requestee_description": request.json["requestee_description"],
            "read": False,
        }
        if model.add_request(_request):
            return jsonify({"status": True, "message": "Request sent successfully"})
        else:
            return jsonify(
                {"status": False, "error": "[DB-ERROR]:Request sending failed"}
            )

    def get(self):
        id = request.args.get("id")
        read = request.args.get("read")
        if id is None:
            return jsonify({"payload": model.get_all_requests()})
        elif read is None:
            return jsonify(
                {
                    "status": model.remove_request(id),
                    "message": "Request removed successfully",
                }
            )
        else:
            return jsonify(
                {"status": model.read_request(id), "message": "Request marked as read"}
            )


if __name__ == "__main__":
    app.run(debug=True)
