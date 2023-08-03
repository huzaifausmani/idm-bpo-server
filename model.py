from bson import json_util, ObjectId
import json


class Model:
    mongo = ""
    comments = ""
    admin = ""
    contact_info = ""
    pics = ""

    def initialize_collections(self):
        self.comments = self.mongo.comments
        self.admin = self.mongo.admin
        self.contact_info = self.mongo.contact_info
        self.pics = self.mongo.pics

    @staticmethod
    def convert_bson_to_json(data):
        return json.loads(json_util.dumps(data))

    # retrievers / getters
    def get_all_comments(cls):
        return cls.convert_bson_to_json(cls.comments.find())

    def get_all_pics(cls):
        return cls.convert_bson_to_json(cls.pics.find())

    def get_contact_info(cls):
        return cls.convert_bson_to_json(cls.contact_info.find())[0]

    def get_admin_info(cls):
        return cls.convert_bson_to_json(cls.admin.find())[0]

    # insertors / setters
    def add_comment(cls, comment):
        cls.comments.insert_one(comment)
        return True

    def add_slider_image(cls, img):
        result = cls.pics.insert_one(img)
        return result.inserted_id

    # updators
    def update_admin_info(cls, admin_info):
        cls.admin.update_one(
            {"_id": ObjectId("64ca82f82fe928929f9803e4")},
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
            {"_id": ObjectId("64c7cf8c3908f37c5a8f5ae1")},
            {
                "$set": {
                    "mail": contact_info["mail"],
                    "telephone": contact_info["telephone"],
                }
            },
        )
        return True

    # deleters / removers
    def remove_pic(cls, id):
        cls.pics.delete_one({"_id": ObjectId(id)})
        return True
