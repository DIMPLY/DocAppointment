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
        #if db.execute('select id from {}s where firstname=\'{}\' and lastname=\'{}\''.format(self.category, firstname, lastname)):
        #    return {'success': False, 'reason':'{} already in database.'.format(self.category.capitalize())}
        newid = db.execute("select uuid_generate_v3(uuid_generate_v1(),\'{}\')".format(firstname))[0]['uuid_generate_v3']
        query = 'insert into {}s values (\'{}\', \'{}\', \'{}\')'.format(self.category, newid, firstname, lastname)
        res = db.execute(query, post=True)
        return {'success': res==1, 'affectedrows': res, 'id': newid}

    def delete(self):
        parser.add_argument('roleid', type=str)
        roleid = parser.parse_args()['roleid']
        res = db.execute('delete from prescriptions where {}id=\'{}\''.format(self.category, roleid), post=True)
        if isinstance(res, int) or res == "no results to fetch":
            res = db.execute('delete from appointments where {}id=\'{}\''.format(self.category, roleid), post=True)
            if isinstance(res, int) or res == "no results to fetch":
                res = db.execute('delete from {}s where id=\'{}\''.format(self.category, roleid), post=True)
        success = res==1
        return {'success': success, 'affectedrows': res}

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
