from flask_restful import Resource, reqparse
from database import DataBase
db = DataBase()
parser = reqparse.RequestParser()
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

    def post(self):
        parser.add_argument('doctorid', type=str)
        parser.add_argument('patientid', type=str)
        parser.add_argument('date', type=str)
        parser.add_argument('start', type=str)
        parser.add_argument('end', type=str)
        args = parser.parse_args()
        query = 'insert into appointments values (\'{}\', \'{}\', 1, \'{}\', \'{}\', \'{}\')'.format(args['doctorid'], args['patientid'], args['date'], args['start'], args['end'])
        res = db.execute(query, post=True)
        return {'success': res==1, 'affectedrows': res}

    def put(self, status):
        parser.add_argument('doctorid')
        parser.add_argument('date')
        parser.add_argument('start')
        args = parser.parse_args()
        statusdict = {'finished':2, 'unattended':0, 'booked':1}
        query = 'update appointments set status={} where doctorid=\'{}\' and date=\'{}\' and starttime=\'{}\''.format(statusdict[status], args['doctorid'], args['date'], args['start'])
        res = db.execute(query, post=True)
        return {'success': res==1, 'affectedrows': res}

class Roles(Resource):
    def get(self):
        query = 'select * from {}s'.format(self.category)
        return db.execute(query)

    def post(self):
        parser.add_argument('firstname', type=str)
        parser.add_argument('lastname', type=str)
        args = parser.parse_args()
        firstname, lastname = args['firstname'], args['lastname']
        if db.execute('select 1 from {}s where firstname=\'{}\' and lastname=\'{}\''.format(self.category, firstname, lastname)):
            return {'success': False, 'reason':'{} already in database.'.format(self.category.capitalize())}
        query = 'insert into {cat}s values (uuid_generate_v3(uuid_generate_v1(),\'{fn}\'), \'{fn}\', \'{ln}\')'.format(cat=self.category, fn=firstname, ln=lastname)
        res = db.execute(query, post=True)
        return {'success': res==1, 'affectedrows': res}

    def delete(self):
        parser.add_argument('roleid', type=str)
        args = parser.parse_args()
        query = 'delete from {}s where id=\'{}\''.format(self.category, args['roleid'])
        res = db.execute(query, post=True)
        return {'success': res==1, 'affectedrows': res}

    def put(self):
        parser.add_argument('id', required=True)
        parser.add_argument('firstname')
        parser.add_argument('lastname')
        args = parser.parse_args()
        first, last = args['firstname'], args['lastname']
        query = ('update {}s set '.format(self.category)) + ('firstname=\'{}\' '.format(first) if first else '') + ('and ' if first and last else '') + ('lastname=\'{}\' '.format(last) if last else '') + 'where id=\'{}\''.format(args['id'])
        print(query)
        res = db.execute(query, post=True)
        return {'success': res==1, 'affectedrows': res}

class Patients(Roles):
    category = 'patient'

class Doctors(Roles):
    category = 'doctor'
