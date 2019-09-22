from flask import Flask #, request
from flask_cors import CORS #, cross_origin
from flask_restful import Api
from roles import Doctors, Patients
from services import Appointments, Prescriptions, Slots 

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route("/")
def hello():
    return {'text':'Hello World!'}

api.add_resource(Appointments, '/appointment', '/appointment/<role>', '/appointment/update/<status>')
api.add_resource(Prescriptions, '/prescription', '/prescription/<role>')
api.add_resource(Doctors, '/doctor')
api.add_resource(Patients, '/patient')
api.add_resource(Slots, '/slots/<doctorid>')

if __name__ == '__main__':
   app.run(port=5002)
