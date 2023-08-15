from bson import json_util, ObjectId
import json


class Model:
    mongo = ""
    admin = ""
    contact_info = ""
    pics = ""
    requests = ""
    comments = ""
    services = ""

    def initialize_collections(self):
        self.admin = self.mongo.admin
        self.contact_info = self.mongo.contact_info
        self.pics = self.mongo.pics
        self.requests = self.mongo.requests
        self.comments = self.mongo.comments
        self.services = self.mongo.services

    @staticmethod
    def convert_bson_to_json(data):
        return json.loads(json_util.dumps(data))

    # retrievers / getters
    def get_admin_info(cls):
        return cls.convert_bson_to_json(cls.admin.find())[0]

    def get_contact_info(cls):
        return cls.convert_bson_to_json(cls.contact_info.find())[0]

    def get_all_pics(cls):
        return cls.convert_bson_to_json(cls.pics.find())

    def get_all_comments(cls):
        return cls.convert_bson_to_json(cls.comments.find())

    def get_all_services(cls):
        return cls.convert_bson_to_json(cls.services.find())

    def get_all_requests(cls):
        return cls.convert_bson_to_json(cls.requests.find())

    def get_requests_by_category(cls, category):
        return cls.convert_bson_to_json(cls.requests.find({"category": category}))

    # insertors / setters
    def add_slider_image(cls, img):
        result = cls.pics.insert_one(img)
        return result.inserted_id

    def add_comment(cls, comment):
        result = cls.comments.insert_one(comment)
        return result.acknowledged

    def add_service(cls, service):
        result = cls.services.insert_one(service)
        return result.acknowledged

    def add_request(cls, request):
        result = cls.requests.insert_one(request)
        return result.acknowledged

    # updators
    def update_admin_info(cls, admin_info):
        cls.admin.update_one(
            {"_id": ObjectId("64db05feaa8250e37195c4cb")},
            {
                "$set": {
                    "username": admin_info["username"],
                    "password": admin_info["password"],
                }
            },
        )
        return True

    def update_contact_info(cls, contact_info):
        cls.contact_info.update_one(
            {"_id": ObjectId("64db0689aa8250e37195c4cc")},
            {
                "$set": {
                    "mail": contact_info["mail"],
                    "telephone": contact_info["telephone"],
                }
            },
        )
        return True

    def read_request(cls, id):
        result = cls.requests.update_one(
            {"_id": ObjectId(id)}, {"$set": {"read": True}}
        )
        return result.acknowledged

    # deleters / removers
    def remove_pic(cls, id):
        result = cls.pics.delete_one({"_id": ObjectId(id)})
        return result.acknowledged

    def remove_comment(cls, id):
        result = cls.comments.delete_one({"_id": ObjectId(id)})
        return result.acknowledged

    def remove_service(cls, id):
        result = cls.services.delete_one({"_id": ObjectId(id)})
        return result.acknowledged

    def remove_request(cls, id):
        result = cls.requests.delete_one({"_id": ObjectId(id)})
        return result.acknowledged
