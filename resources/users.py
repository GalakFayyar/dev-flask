import json

class User():
    def get_all(self):
        data = json.load(open('data/utilisateurs.json'))
        return data
