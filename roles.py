from flask_restful import Resource, reqparse
from database import DataBase
db = DataBase()
parser = reqparse.RequestParser()

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
