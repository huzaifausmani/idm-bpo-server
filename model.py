from bson import json_util, ObjectId
import json


class Model:
    mongo = ""
    comments = ""
    admin = ""
    contact_info = ""

    def initialize_collections(self):
        self.comments = self.mongo.comments
        self.admin = self.mongo.admin
        self.contact_info = self.mongo.contact_info

    @staticmethod
    def convert_bson_to_json(data):
        return json.loads(json_util.dumps(data))

    def get_all_comments(cls):
        return cls.convert_bson_to_json(cls.comments.find())

    def get_admin(cls):
        return cls.convert_bson_to_json(cls.admin.find())

    def get_contact_info(cls):
        return cls.convert_bson_to_json(cls.contact_info.find())[0]

    def get_admin_info(cls):
        return cls.convert_bson_to_json(cls.admin.find())[0]

    def add_comment(cls, comment):
        cls.comments.insert_one(comment)
        return True

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
