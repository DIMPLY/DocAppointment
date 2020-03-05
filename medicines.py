from flask_restful import Resource
from database import DataBase
db = DataBase()

class Medicines(Resource):
    def get(self):
        query = 'select * from medicines'
        return db.execute(query)

