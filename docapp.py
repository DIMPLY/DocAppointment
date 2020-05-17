import db_init
from flask import Flask #, request
from flask_cors import CORS #, cross_origin
from flask_restful import Api
from roles import Doctors, Patients, Login
from services import Appointments, Prescriptions, Slots
from medicines import Medicines

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/")
def hello():
    return {'text':'Hello World!'}

api.add_resource(Appointments, '/appointment', '/appointment/<role>', '/appointment/update/<status>')
api.add_resource(Prescriptions, '/prescription', '/prescription/<role>')
api.add_resource(Doctors, '/doctor')
api.add_resource(Patients, '/patient')
api.add_resource(Login, '/patient/login')
api.add_resource(Slots, '/slots/<doctorid>')
api.add_resource(Medicines, '/medicine')

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5002)
