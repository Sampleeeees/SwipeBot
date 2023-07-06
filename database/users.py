from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient, IndexModel

from config.config_reader import config

client = MongoClient(config.mongo_url)
mydb = client[config.mongo_db]

mydb.users.create_indexes([
    IndexModel('user_id', unique=True)
])


class User:
    def __init__(self, user_id, token, refresh_token, is_auth, language=None):
        self.user_id = user_id
        self.token = token
        self.refresh_token = refresh_token
        self.is_auth = is_auth
        self.language = language

    def save(self):
        user_data = {
            'user_id': self.user_id,
            'token': self.token,
            'refresh_token': self.refresh_token,
            'is_auth': self.is_auth,
            'language': self.language
        }
        try:
            mydb.users.insert_one(user_data)
        except DuplicateKeyError:
            raise ValueError("Користувач з таким ідентифікатором вже існує")

    @staticmethod
    def find_user(user_id):
        user = mydb.users.find_one({"user_id": user_id})
        if user:
            return user
        return None

    def update(self):
        mydb.users.update_one(
            {"user_id": self.user_id},
            {"$set": {
                "token": self.token,
                "refresh_token": self.refresh_token,
                "is_auth": self.is_auth,
                "language": self.language
            }}
        )