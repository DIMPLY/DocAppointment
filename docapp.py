from flask import Flask #, request
from flask_cors import CORS #, cross_origin
from flask_restful import Api
from resources import Appointments, Doctors, Patients

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route("/")
def hello():
    return {'text':'Hello World!'}

api.add_resource(Appointments, '/appointment/<subject>/<subjectid>', '/appointment', '/appointment/<status>')
api.add_resource(Doctors, '/doctor')
api.add_resource(Patients, '/patient')

if __name__ == '__main__':
   app.run(port=5002)
