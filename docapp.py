from flask import Flask #, request
from flask_cors import CORS #, cross_origin
from flask_restful import Resource, Api

from database import DataBase

app = Flask(__name__)
api = Api(app)
db = DataBase()

CORS(app)

@app.route("/")
def hello():
    return {'text':'Hello World!'}

class Appointments(Resource):
    def get(self, subject, subjectid):
        query = '''
                select a.doctorid,
                       d.firstname as doc_first,
                       d.lastname as doc_last,
                       a.patientid,
                       p.firstname as pat_first,
                       p.lastname as pat_last,
                       a.status,
                       to_char(a.date, \'yyyy-mm-dd\') as date,
                       to_char((a.starttime at time zone \'utc\')::time, \'hh24:mi:ss\') as starttime,
                       to_char((a.endtime at time zone \'utc\')::time, \'hh24:mi:ss\') as endtime
          from appointments as a
          left join doctors as d on a.doctorid=d.id
          left join patients as p on a.patientid=p.id
          where {}.id='{}'
          '''.format('d' if subject=='doctor' else 'p', subjectid)
        return db.execute(query)


class Doctors(Resource):
    def get(self):
        query = 'select * from doctors'
        return db.execute(query)

    def post(self, firstname, lastname):
        if db.execute('select 1 from doctors where firstname=\'{}\' and lastname=\'{}\''.format(firstname, lastname)):
            return {'success': False, 'reason':'Doctor already in database.'}
        query = 'insert into doctors values (uuid_generate_v1(), \'{}\', \'{}\')'.format(firstname, lastname)
        return {'success': db.execute(query, post=True)!=0}


api.add_resource(Appointments, '/appointments/<subject>/<subjectid>')
api.add_resource(Doctors, '/doctors', '/doctor/<firstname>/<lastname>')
#api.add_resource(DoctorNew, '/doctor/<firstname>/<lastname>')

if __name__ == '__main__':
   app.run(port=5002)
