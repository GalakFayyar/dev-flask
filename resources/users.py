import json

class User():
    def __init__(self, data):
        self.data = data

    def get_users(self):
        data = json.load(open('../data/utilisateurs.json'))

        return data